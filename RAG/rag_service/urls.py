# urls.py
from django.urls import path
from .views import DocumentProcessingView, GetBestMatchView

urlpatterns = [
    path("api/process_document/", DocumentProcessingView.as_view(), name="process-document"),
    path("api/get_best_match/", GetBestMatchView.as_view(), name="get-best-match"),
]
