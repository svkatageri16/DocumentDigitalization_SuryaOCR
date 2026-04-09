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
os.makedirs(EXTRACTED_DIR, exist_ok=True)
os.makedirs("uploads", exist_ok=True)

_embedder = None

def get_embedder():
    global _embedder
    if _embedder is None:
        print("[Utils] Loading multilingual embedder...")
        _embedder = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
    return _embedder

# ====================== PHASE 1: OCR ======================
def extract_and_purge(file_path: str):
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
            print(f"[2/5] Processing PDF → {total_pages} pages (one by one)")

            for page_num in range(total_pages):
                print(f"   → Page {page_num + 1}/{total_pages}")
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap(dpi=200)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                # Run OCR
                predictions = recognition_predictor([img], det_predictor=detection_predictor)

                full_extracted_text += f"\n--- START OF PAGE {page_num + 1} ---\n\n"
                for pred in predictions:
                    for line in pred.text_lines:
                        full_extracted_text += line.text + "\n"
                full_extracted_text += f"\n--- END OF PAGE {page_num + 1} ---\n"

                # Aggressive cleanup after every page
                del img, pix, page, predictions
                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                    torch.cuda.synchronize()   # ← Added for better release

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
        # FINAL STRONG CLEANUP - Most Important Part
        print("[4/5] Releasing Surya OCR from GPU VRAM...")
        del foundation_predictor, recognition_predictor, detection_predictor
        gc.collect()

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()   # Force GPU to finish operations
            print(f"   GPU Memory after cleanup: {torch.cuda.memory_allocated()/1024**2:.1f} MB allocated")

    # Save extracted text
    timestamp = int(time.time())
    output_filename = os.path.join(EXTRACTED_DIR, f"Extracted_{filename}_{timestamp}.txt")
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(full_extracted_text)

    print(f"[*] OCR completed and GPU released → {output_filename}")
    return full_extracted_text.strip()

# ====================== PHASE 2: STORAGE ======================
def store_data(text: str):
    print("\n[5/5] Generating embeddings → ChromaDB")
    embedder = get_embedder()

    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        chroma_client.delete_collection("offline_docs")
    except:
        pass

    collection = chroma_client.create_collection(name="offline_docs")

    chunk_size = 400
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    embeddings = embedder.encode(chunks).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(documents=chunks, embeddings=embeddings, ids=ids)
    print(f"✅ Stored {len(chunks)} chunks")
    return collection

# ====================== PHASE 3: QUERY ======================
def process_query(user_query: str):
    if not user_query.strip():
        return "Please ask a question."

    embedder = get_embedder()
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

    try:
        collection = chroma_client.get_collection("offline_docs")
    except Exception:
        return ":x: No document has been processed yet. Please upload and process a PDF/image first."

    try:
        query_embedding = embedder.encode(user_query).tolist()
        results = collection.query(query_embeddings=[query_embedding], n_results=5)

        context = "\n\n".join(results.get('documents', [[]])[0]) if results.get('documents') else ""

        if not context.strip():
            return "I could not find any relevant information in the document for your query."

        system_prompt = f"""You are a highly intelligent, multilingual assistant.
Answer the user's question based ONLY on the provided document context.
If the answer is not present in the context, clearly say "I could not find this information in the document."

DOCUMENT CONTEXT:
{context}
"""

        response = ollama.chat(
            model='qwen3:8b',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_query}
            ]
        )

        return response['message']['content']

    except Exception as e:
        print(f"[ERROR in process_query]: {str(e)}")
        import traceback
        traceback.print_exc()
        return f":x: An error occurred while processing your query: {str(e)}\n\nPlease make sure Ollama is running and the model 'qwen3:8b' is downloaded."