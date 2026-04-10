from django.urls import path
from . import views

urlpatterns = [
    # Web Pages
    path('', views.upload_page, name='home'),
    path('upload/', views.upload_page, name='upload_page'),
    path('chat/', views.chat_page, name='chat_page'),

    # API Routes
    path('api/upload/', views.upload_document, name='upload_document'),
    path('api/documents/', views.get_documents, name='get_documents'),
    path('api/query/', views.query_document, name='query_document'),
    path('api/delete/', views.delete_document_view, name='delete_document'),
    path('api/progress/', views.get_processing_status, name='get_processing_status'),
]