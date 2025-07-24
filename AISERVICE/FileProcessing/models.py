from django.db import models
from projects.models import Project
# Create your models here.

class Document(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


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
