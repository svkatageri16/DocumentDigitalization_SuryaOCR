from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from .utils import extract_and_purge, store_data, process_query

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
            text = extract_and_purge(file_path)
            store_data(text)
            os.remove(file_path)  # clean up uploaded file
            return JsonResponse({
                'status': 'success',
                'message': 'Document processed successfully!',
                'filename': uploaded_file.name,
                'preview': text[:500] + '...' if len(text) > 500 else text
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@csrf_exempt
def query_document(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        query = data.get('query', '')
        response = process_query(query)
        return JsonResponse({'status': 'success', 'response': response})
    return JsonResponse({'status': 'error'}, status=400)


def home(request):
    return render(request, 'index.html')