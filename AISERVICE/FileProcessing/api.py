# documents/api.py
from rest_framework import viewsets
from .models import Document, Chunk, Embedding
from .serializers import DocumentSerializer, ChunkSerializer, EmbeddingSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class ChunkViewSet(viewsets.ModelViewSet):
    queryset = Chunk.objects.all()
    serializer_class = ChunkSerializer


class EmbeddingViewSet(viewsets.ModelViewSet):
    queryset = Embedding.objects.all()
    serializer_class = EmbeddingSerializer
