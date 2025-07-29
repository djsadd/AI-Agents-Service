# urls.py
from django.urls import path
from .views import DocumentProcessingView

urlpatterns = [
    path("api/process_document/", DocumentProcessingView.as_view(), name="process-document"),
]
