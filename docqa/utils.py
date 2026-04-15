import os
import gc
import torch
import chromadb
import ollama
import fitz
from sentence_transformers import SentenceTransformer
from PIL import Image
import time
from surya.foundation import FoundationPredictor
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor

CHROMA_PATH = "./chroma_storage"
EXTRACTED_DIR = "./extracted_documents"
CHROMA_COLLECTION_NAME = "cp_permanent_docs"

os.makedirs(EXTRACTED_DIR, exist_ok=True)
os.makedirs("uploads", exist_ok=True)

_embedder = None

def get_embedder():
    global _embedder
    if _embedder is None:
        print("[Utils] Loading multilingual embedder...")
        _embedder = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
    return _embedder

def get_chroma_collection():
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    return chroma_client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

# ====================== PHASE 1: OCR ======================
def extract_and_purge(file_path: str):
    # (Your original function - unchanged, only minor cleanup improvements)
    print("\n[1/5] Loading Surya OCR into GPU...")
    foundation_predictor = FoundationPredictor()
    recognition_predictor = RecognitionPredictor(foundation_predictor)
    detection_predictor = DetectionPredictor()
    full_extracted_text = ""
    filename = os.path.basename(file_path)

    try:
        if file_path.lower().endswith('.pdf'):
            pdf_document = fitz.open(file_path)
            total_pages = len(pdf_document)
            print(f"[2/5] Processing PDF → {total_pages} pages")
            for page_num in range(total_pages):
                print(f" → Page {page_num + 1}/{total_pages}")
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap(dpi=200)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                predictions = recognition_predictor([img], det_predictor=detection_predictor)
                full_extracted_text += f"\n--- START OF PAGE {page_num + 1} ---\n\n"
                for pred in predictions:
                    for line in pred.text_lines:
                        full_extracted_text += line.text + "\n"
                full_extracted_text += f"\n--- END OF PAGE {page_num + 1} ---\n"
                del img, pix, page, predictions
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
        else:
            print("[2/5] Processing Image...")
            img = Image.open(file_path)
            predictions = recognition_predictor([img], det_predictor=detection_predictor)
            for pred in predictions:
                for line in pred.text_lines:
                    full_extracted_text += line.text + "\n"
            del img, predictions
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
    finally:
        print("[4/5] Releasing Surya OCR from GPU...")
        del foundation_predictor, recognition_predictor, detection_predictor
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

    # Save extracted text
    timestamp = int(time.time())
    output_filename = os.path.join(EXTRACTED_DIR, f"Extracted_{filename}_{timestamp}.txt")
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(full_extracted_text)
    print(f"[*] OCR completed → {output_filename}")
    return full_extracted_text.strip()

# ====================== NEW: PROCESS UPLOAD (Skip if exists) ======================
def process_uploaded_document(file_path: str, uploaded_filename: str):
    original_name = os.path.splitext(uploaded_filename)[0]
    collection = get_chroma_collection()

    # Check if document already exists
    existing = collection.get(where={"source_file": original_name})
    if existing and len(existing.get('ids', [])) > 0:
        print(f"[SUCCESS] '{original_name}' already in database → skipping OCR")
        return {
            'status': 'exists',
            'original_name': original_name,
            'message': 'Document already processed and available in database.'
        }

    # New document → run OCR
    text = extract_and_purge(file_path)

    # Store permanently with metadata
    print("\n[5/5] Generating embeddings → Permanent ChromaDB")
    embedder = get_embedder()
    chunk_size = 400
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    embeddings = embedder.encode(chunks).tolist()
    ids = [f"{original_name}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source_file": original_name} for _ in range(len(chunks))]

    collection.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)
    print(f":white_check_mark: Stored {len(chunks)} chunks for {original_name}")

    del embedder
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return {
        'status': 'success',
        'original_name': original_name,
        'text_preview': text[:500] + '...' if len(text) > 500 else text
    }

# ====================== NEW: QUERY WITH DOCUMENT FILTER + MEMORY ======================
def process_query(user_query: str, document_name: str, history: list = None):
    if not user_query.strip():
        return "Please ask a question."
    if history is None:
        history = []

    print(f"[DEBUG process_query] user_query='{user_query[:50]}...', document_name='{document_name}'")
    
    embedder = get_embedder()
    collection = get_chroma_collection()

    try:
        query_embedding = embedder.encode(user_query).tolist()
        print(f"[DEBUG process_query] Querying ChromaDB with source_file='{document_name}'")
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5,
            where={"source_file": document_name}
        )
        print(f"[DEBUG process_query] Query results: {len(results.get('documents', [[]])[0])} documents found")
        context = "\n\n".join(results.get('documents', [[]])[0]) if results.get('documents') else ""

        if not context.strip():
            print(f"[DEBUG process_query] No context found for document '{document_name}'")
            print(f"[DEBUG process_query] Available source_files in DB:")
            all_results = collection.get()
            unique_sources = set()
            for metadata in all_results.get('metadatas', []):
                unique_sources.add(metadata.get('source_file'))
            for source in sorted(unique_sources):
                print(f"  - {source}")
            return "I could not find any relevant information in the selected document."

        system_prompt = f"""You are a highly intelligent, multilingual assistant for CP Office, Pune.
Answer the user's question based ONLY on the provided document context.
If the answer is not present in the context, clearly say "I could not find this information in the document."
Be professional, precise and helpful. Use Marathi when the query is in Marathi.

DOCUMENT CONTEXT:
{context}
"""

        messages = [{'role': 'system', 'content': system_prompt}]
        messages.extend(history)
        messages.append({'role': 'user', 'content': user_query})

        print(f"[DEBUG process_query] Sending request to Ollama with {len(messages)} messages")
        response = ollama.chat(
            model='qwen3:8b',
            messages=messages
        )
        print(f"[DEBUG process_query] Ollama response received")
        return response['message']['content']

    except Exception as e:
        print(f"[ERROR in process_query]: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"An error occurred: {str(e)}"