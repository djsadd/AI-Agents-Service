from django.db import models
from projects.models import Project
# Create your models here.

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



class Chunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    text = models.TextField()
    chunk_index = models.PositiveIntegerField()

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.title}"


from django.contrib.postgres.fields import ArrayField

class Embedding(models.Model):
    chunk = models.OneToOneField(Chunk, on_delete=models.CASCADE, related_name='embedding')
    vector = ArrayField(models.FloatField(), size=768)  # Или 1536 для OpenAI, зависит от модели

    def __str__(self):
        return f"Embedding for chunk {self.chunk.id}"
