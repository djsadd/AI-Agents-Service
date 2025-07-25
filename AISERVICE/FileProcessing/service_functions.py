'''extract_text(document_file) – извлечь текст из PDF, DOCX, TXT.

split_text(text) – разбить на чанки (например, по 500 токенов).

get_embedding(chunk_text) – вызвать OpenAI или другую модель для создания эмбеддинга.

store_in_quadrant(project_id, chunk_id, vector) – сохранить в Quadrant (или любую векторную БД).

'''

import uuid
import requests

from sentence_transformers import SentenceTransformer
from typing import List
import fitz  # PyMuPDF
from docx import Document
import os


def extract_text(file_path):
    _, ext = os.path.splitext(file_path)

    if ext.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext.lower() == ".docx":
        return extract_text_from_docx(file_path)
    elif ext.lower() == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

import re

def split_text(text, chunk_size=500, overlap=50):
    # Разделим по пробелам на слова (можно заменить на токены позже)
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks


embedding_model = SentenceTransformer('BAAI/bge-base-en-v1.5')

def get_embeddings(text_chunks: List[str]) -> List[List[float]]:
    """
    Получает эмбеддинги для списка текстов (чанков).
    """
    embeddings = embedding_model.encode(
        text_chunks,
        normalize_embeddings=True,
        show_progress_bar=True
    )
    return embeddings


QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "my_collection"


QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "my_collection"
VECTOR_SIZE = 768  # размерность эмбеддингов, поменяй если у тебя другая

def ensure_qdrant_collection():
    """Проверяет наличие коллекции в Qdrant и создаёт её при необходимости."""
    url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}"

    # Проверка: существует ли коллекция
    resp = requests.get(url)
    if resp.status_code == 200:
        print("ℹ️ Коллекция уже существует.")
        return
    elif resp.status_code != 404:
        print(f"❌ Ошибка при проверке коллекции: {resp.text}")
        return

    # Создание коллекции
    payload = {
        "vectors": {
            "size": VECTOR_SIZE,
            "distance": "Cosine"
        }
    }
    create_resp = requests.put(url, json=payload)
    if create_resp.status_code == 200:
        print("✅ Коллекция успешно создана.")
    else:
        print(f"❌ Ошибка при создании коллекции: {create_resp.text}")


def upload_to_qdrant(embeddings, texts, file_id):
    """
    Загружает чанки с эмбеддингами в Qdrant.
    """
    ensure_qdrant_collection()  # ← добавили создание коллекции

    url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points"

    points = []
    for vector, text in zip(embeddings, texts):
        point = {
            "id": str(uuid.uuid4()),
            "vector": vector.tolist(),  # ← добавлено .tolist()
            "payload": {
                "text": text,
                "file_id": file_id
            }
        }
        points.append(point)

    payload = {
        "points": points
    }

    try:
        response = requests.put(url, json=payload)
        response.raise_for_status()
        print(f"✅ Загружено {len(points)} точек в Qdrant.")
    except Exception as e:
        print(f"❌ Ошибка при загрузке в Qdrant: {e}")

TEST_FILE_PATH = r"C:\Users\User\Desktop\AI-Agents-Service\AISERVICE\tests files\test.docx"

def test_pipeline():
    print("🔍 Тестируем pipeline на файле:", TEST_FILE_PATH)

    # 1. Чтение текста
    text = extract_text(TEST_FILE_PATH)
    assert isinstance(text, str) and len(text) > 0, "❌ Текст не извлечён"

    # 2. Разбиение
    chunks = split_text(text)
    assert isinstance(chunks, list) and len(chunks) > 0, "❌ Чанки не созданы"
    print(f"✅ Получено {len(chunks)} чанков")

    # 3. Эмбеддинги
    embeddings = get_embeddings(chunks)
    assert len(embeddings) == len(chunks), "❌ Эмбеддингов не столько же, сколько чанков"
    assert len(embeddings[0]) == 768, "❌ Размер эмбеддинга не 768"
    print("✅ Эмбеддинги сгенерированы")

    # 4. Загрузка в Qdrant
    upload_to_qdrant(embeddings, chunks, file_id="test_file_for_pipeline")
    print("✅ Все данные успешно загружены в Qdrant")

if __name__ == "__main__":
    test_pipeline()
