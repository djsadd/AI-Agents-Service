from django.shortcuts import render
from .models import Document, Chunk, Embedding
# Create your views here.
# views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from django.shortcuts import render
from services.embeddings.store import get_best_match
from .models import Document
from projects.models import Project

from llm.views import ask_groq


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

def ask_question_view(request):
    context = {}

    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            best_match = get_best_match(question)

            if best_match and "text" in best_match:
                retrieved_context = best_match["text"]

                # ❗ Вот здесь вызывается твоя функция
                llm_answer = ask_groq(retrieved_context, question)

                context['question'] = question
                context['answer'] = llm_answer
                context['retrieved_context'] = retrieved_context
                context['source'] = best_match.get('file_id', 'N/A')  # если хочешь
            else:
                context['answer'] = "❌ Ничего не найдено в базе знаний."

    return render(request, 'fileprocessing/ask.html', context)
