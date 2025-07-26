# projects/urls.py
from django.urls import path
from .views import ProjectCreateView, ProjectsListView

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('list/', ProjectsListView.as_view(), name='project_list'),
]
