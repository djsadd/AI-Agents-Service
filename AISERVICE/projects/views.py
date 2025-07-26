# views.py
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import ListView
from .models import Project


@method_decorator(login_required, name='dispatch')
class ProjectCreateView(View):
    def get(self, request):
        return render(request, 'projects/create.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description', '')

        if not name:
            messages.error(request, "Название проекта обязательно.")
            return redirect(request.path)

        project = Project.objects.create(
            name=name,
            description=description,
            owner=request.user
        )

        messages.success(request, f"Проект «{project.name}» успешно создан.")
        return redirect('document_upload', project_id=project.id)  # ← после создания переходим к загрузке


class ProjectsListView(ListView):
    model = Project
    template_name = "projects/list.html"