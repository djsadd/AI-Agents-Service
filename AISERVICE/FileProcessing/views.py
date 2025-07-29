# Create your views here.
# views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from django.shortcuts import render
from .models import Document
from projects.models import Project


class DocumentUploadView(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        return render(request, 'fileprocessing/upload.html', {'project': project})

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            messages.error(request, "Файл не загружен.")
            return redirect(request.path)

        # Создаём объект Document
        document = Document.objects.create(
            project=project,
            file=uploaded_file,
            original_filename=uploaded_file.name
        )

        try:
            document.process()  # Запускаем пайплайн
            messages.success(request, "Документ успешно загружен и обработан.")
        except Exception as e:
            messages.error(request, f"Ошибка при обработке: {str(e)}")

        return redirect(request.path)

