from django.shortcuts import render
from .models import Document, Chunk, Embedding
# Create your views here.

def upload_document(project, file):
    doc = Document.objects.create(project=project, file=file)
    return doc

def split_into_chunks(document):
    text = extract_text(document.file.path)  # extract from PDF/DOCX/etc
    chunks = split_text(text, chunk_size=500)
    chunk_objects = [Chunk(document=document, content=c) for c in chunks]
    Chunk.objects.bulk_create(chunk_objects)
    return chunk_objects


def create_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        vector = get_embedding(chunk.content)  # call LLM API
        emb = Embedding.objects.create(chunk=chunk, vector=vector)
        store_in_quadrant(vector, metadata={"chunk_id": chunk.id})
        embeddings.append(emb)
    return embeddings