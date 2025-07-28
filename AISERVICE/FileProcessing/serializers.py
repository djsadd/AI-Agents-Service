from rest_framework import serializers
from .models import Document, Chunk, Embedding


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class ChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chunk
        fields = '__all__'


class EmbeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Embedding
        fields = '__all__'
