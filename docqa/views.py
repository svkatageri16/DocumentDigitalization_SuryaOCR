from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from .utils import process_uploaded_document, process_query
from .models import ProcessedDocument

@csrf_exempt
def upload_document(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'status': 'error', 'message': 'No file uploaded'}, status=400)

        uploaded_file = request.FILES['file']
        file_path = os.path.join('uploads', uploaded_file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        try:
            result = process_uploaded_document(file_path, uploaded_file.name)
            os.remove(file_path)

            # Always ensure model entry exists
            original_name = result.get('original_name') or os.path.splitext(uploaded_file.name)[0]
            ProcessedDocument.objects.get_or_create(
                original_filename=original_name,
                defaults={
                    'display_name': uploaded_file.name,
                    'file_type': 'pdf' if uploaded_file.name.lower().endswith('.pdf') else 'image'
                }
            )

            return JsonResponse({
                'status': 'success',
                'message': result.get('message', 'Document processed successfully!'),
                'filename': uploaded_file.name,
                'preview': result.get('text_preview', 'Ready for chat'),
                'original_name': original_name
            })
        except Exception as e:
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


def upload_page(request):
    return render(request, 'upload.html')


def chat_page(request):
    return render(request, 'chat.html')