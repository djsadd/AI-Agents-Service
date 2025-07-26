# urls.py
from django.urls import path
from .views import DocumentUploadView, ask_question_view

urlpatterns = [
    path('upload/<int:project_id>/', DocumentUploadView.as_view(), name='document_upload'),
    path('ask/', ask_question_view, name='ask-question'),

]
