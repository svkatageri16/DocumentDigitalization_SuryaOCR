from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from .utils import process_uploaded_document, process_query, delete_document
from .models import ProcessedDocument

# Global dict for progress (simple solution for development)
processing_status = {}

@csrf_exempt
def upload_document(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'status': 'error', 'message': 'No file uploaded'}, status=400)

        uploaded_file = request.FILES['file']
        file_path = os.path.join('uploads', uploaded_file.name)
        original_name = os.path.splitext(uploaded_file.name)[0]

        # Initialize progress
        processing_status[original_name] = {'progress': 5, 'message': 'Uploading file...'}

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        try:
            processing_status[original_name] = {'progress': 20, 'message': 'Checking if document already exists...'}

            result = process_uploaded_document(file_path, uploaded_file.name)
            
            processing_status[original_name] = {'progress': 90, 'message': 'Finalizing storage...'}

            os.remove(file_path)

            ProcessedDocument.objects.get_or_create(
                original_filename=original_name,
                defaults={
                    'display_name': uploaded_file.name,
                    'file_type': 'pdf' if uploaded_file.name.lower().endswith('.pdf') else 'image'
                }
            )

            processing_status[original_name] = {'progress': 100, 'message': 'Document processed successfully!'}

            return JsonResponse({
                'status': 'success',
                'message': result.get('message', 'Document processed successfully!'),
                'filename': uploaded_file.name,
                'preview': result.get('text_preview', ''),
                'original_name': original_name
            })
        except Exception as e:
            processing_status[original_name] = {'progress': 0, 'message': f'Error: {str(e)}'}
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@csrf_exempt
def get_documents(request):
    if request.method == 'GET':
        docs = ProcessedDocument.objects.all().values(
            'original_filename', 'display_name', 'upload_date', 'file_type'
        )
        return JsonResponse({'status': 'success', 'documents': list(docs)})
    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def query_document(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        query = data.get('query', '')
        document_name = data.get('document_name', '')
        history = data.get('history', [])

        if not document_name:
            return JsonResponse({'status': 'error', 'response': 'Please select a document first.'})

        response = process_query(query, document_name, history)
        return JsonResponse({'status': 'success', 'response': response})

    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def delete_document_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        original_name = data.get('original_name', '')
        if not original_name:
            return JsonResponse({'status': 'error', 'message': 'No document specified'}, status=400)
        
        success = delete_document(original_name)
        if success:
            # Clean progress if any
            if original_name in processing_status:
                del processing_status[original_name]
            return JsonResponse({'status': 'success', 'message': f'Document "{original_name}" deleted successfully.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to delete document.'}, status=500)
    
    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def get_processing_status(request):
    if request.method == 'GET':
        doc_name = request.GET.get('doc_name', '')
        status = processing_status.get(doc_name, {'progress': 0, 'message': 'Idle'})
        return JsonResponse(status)
    return JsonResponse({'status': 'error'}, status=400)


def upload_page(request):
    return render(request, 'upload.html')


def chat_page(request):
    return render(request, 'chat.html')