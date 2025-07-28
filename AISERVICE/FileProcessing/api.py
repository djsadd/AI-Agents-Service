# documents/api.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
