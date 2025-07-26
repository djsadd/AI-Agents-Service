# urls.py
from django.urls import path
from .views import ask_question_view

urlpatterns = [
    path('ask/<int:project_pk>', ask_question_view, name='ask-question'),
]


