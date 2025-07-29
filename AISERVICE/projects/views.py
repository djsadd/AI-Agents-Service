# views.py
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import ListView
from .models import Project
from django.views.generic.edit import CreateView
from .forms import TelegramIntegrationForm, WhatsAppIntegrationForm
from .models import Integration
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


@method_decorator(login_required, name='dispatch')
class ProjectCreateView(View):
    def get(self, request):
        return render(request, 'projects/create.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        system_text = request.POST.get('system_text', '')

        if not name:
            messages.error(request, "Название проекта обязательно.")
            return redirect(request.path)
        if not system_text:
            messages.error(request, "системный текст")
            return redirect(request.path)

        project = Project.objects.create(
            name=name,
            description=description,
            owner=request.user,
            system_text=system_text,
        )

        messages.success(request, f"Проект «{project.name}» успешно создан.")
        return redirect('document_upload', project_id=project.id)  # ← после создания переходим к загрузке


class ProjectsListView(ListView):
    model = Project
    template_name = "projects/list.html"

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)


class IntegrationCreateView(CreateView):
    template_name = 'projects/integration_form.html'

    def get_form_class(self):
        integration_type = self.kwargs.get('type')  # 'telegram' или 'whatsapp'
        if integration_type == 'telegram':
            return TelegramIntegrationForm
        elif integration_type == 'whatsapp':
            return WhatsAppIntegrationForm
        else:
            raise ValueError("Неподдерживаемый тип интеграции")

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('project_list')
