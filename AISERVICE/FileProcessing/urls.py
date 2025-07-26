# urls.py
from django.urls import path
from .views import DocumentUploadView

urlpatterns = [
    path('upload/<int:project_id>/', DocumentUploadView.as_view(), name='document_upload'),

]
