from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/upload/', views.upload_document, name='upload'),
    path('api/query/', views.query_document, name='query'),
]