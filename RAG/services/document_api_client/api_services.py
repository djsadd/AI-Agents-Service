from django.conf import settings
import requests


def create_embedding(vector, chunk_id):
    data = {
        "vector": vector,
        "chunk": chunk_id
    }
    response = requests.post(f"{settings.DOCUMENT_SERVICE_BASE_URL}/embeddings/", json=data)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Ошибка создания эмбеддинга: {response.status_code}, {response.text}")


def create_chunks(document_id, text, chunk_index):
    data = {
        "document": document_id,
        "text": text,
        "chunk_index": chunk_index,
    }
    response = requests.post(f"{settings.DOCUMENT_SERVICE_BASE_URL}/chunks/", json=data)
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Ошибка создания чанка: {response.status_code}, {response.text}")