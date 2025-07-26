from django.db import models
from projects.models import Project
from django.contrib.postgres.fields import ArrayField

from services.utils.extract import extract_text
from services.utils.splitter import split_text
from services.embeddings.encode import get_embeddings
from services.qdrant.uploader import upload_to_qdrant

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

    def process(self):

        try:
            print(f"📄 Обработка документа: {self.original_filename}")
            self.status = 'processing'
            self.save()

            # 1. Извлечение текста
            print("Извлечение текста")
            text = extract_text(self.file.path)
            if not text.strip():
                raise ValueError("Извлечён пустой текст")

            # 2. Разделение на чанки
            print("Разделение на чанки")
            chunks = split_text(text)

            # 3. Сохранение чанков
            print("Сохранение чанков")
            chunk_objs = []
            for idx, chunk_text in enumerate(chunks):
                chunk_objs.append(Chunk(document=self, text=chunk_text, chunk_index=idx))
            Chunk.objects.bulk_create(chunk_objs)
            print(chunk_objs)
            # 4. Эмбеддинги
            print("Эмбеддинги")
            created_chunks = self.chunks.order_by("chunk_index").all()
            chunk_texts = [ch.text for ch in created_chunks]
            embeddings = get_embeddings(chunk_texts)

            # 5. Сохранение эмбеддингов
            print("Сохранение эмбеддингов")
            for chunk, vector in zip(created_chunks, embeddings):
                Embedding.objects.create(chunk=chunk, vector=vector)

            # 6. Загрузка в Qdrant
            print("Загрузка в Qdrant")

            upload_to_qdrant(embeddings, chunk_texts, file_id=str(self.id))

            self.status = 'ready'
            self.error_message = ''
            self.save()
            print("✅ Документ успешно обработан.")
        except Exception as e:
            self.status = 'error'
            self.error_message = str(e)
            self.save()
            print(f"❌ Ошибка при обработке документа: {e}")


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
