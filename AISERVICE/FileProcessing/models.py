from django.db import models
from projects.models import Project
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

# Create your models here.
import requests


class Document(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('error', 'Error'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField(upload_to='documents/')
    original_filename = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_filename

    def process(self):
        api_url = settings.RAG_API_URL

        try:
            with open(self.file.path, 'rb') as f:
                files = {'file': (self.original_filename, f)}
                data = {
                    'file_id': str(self.id),
                    'project_id': self.project.id,
                    'original_filename': self.original_filename,
                }
                response = requests.post(api_url, files=files, data=data)

            if response.status_code == 200:
                print("📤 Обработка запущена во втором сервисе")
            else:
                print(f"❌ Ошибка запуска обработки: {response.status_code}, {response.text}")

        except Exception as e:
            print(f"❌ Ошибка при попытке отправить файл: {e}")


class Chunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    text = models.TextField()
    chunk_index = models.PositiveIntegerField()

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.original_filename}"


class Embedding(models.Model):
    chunk = models.OneToOneField(Chunk, on_delete=models.CASCADE, related_name='embedding')
    vector = ArrayField(models.FloatField(), size=768)  # Или 1536 для OpenAI, зависит от модели

    def __str__(self):
        return f"Embedding for chunk {self.chunk.id}"
