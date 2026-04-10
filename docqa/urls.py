from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_page, name='home'),           # Upload page (default)
    path('upload/', views.upload_page, name='upload'),
    path('chat/', views.chat_page, name='chat'),
    path('api/upload/', views.upload_document, name='upload_api'),
    path('api/documents/', views.get_documents, name='documents_api'),
    path('api/query/', views.query_document, name='query_api'),
]