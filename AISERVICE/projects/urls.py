# projects/urls.py
from django.urls import path
from .views import ProjectCreateView, ProjectsListView, IntegrationCreateView

urlpatterns = [
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('list/', ProjectsListView.as_view(), name='project_list'),
    path('project/<int:pk>/integration/create/<str:type>/', IntegrationCreateView.as_view(), name='integration_create'),
]
