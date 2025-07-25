from django.shortcuts import render
from .models import Project
# Create your views here.

def create_project(user, title, description=""):
    return Project.objects.create(user=user, title=title, description=description)
