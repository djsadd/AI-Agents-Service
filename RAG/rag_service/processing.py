# processing.py

from services.utils.extract import extract_text
from services.utils.splitter import split_text
from services.embeddings.encode import get_embeddings
from services.qdrant.uploader import upload_to_qdrant


def process_document(file_path):
    print(f"📄 Обработка документа: {file_path}")

    # 1. Извлечение текста
    text = extract_text(file_path)
    if not text.strip():
        raise ValueError("Извлечён пустой текст")

    # 2. Разделение на чанки
    chunks = split_text(text)

    # 3. Эмбеддинги
    embeddings = get_embeddings(chunks)

    # 4. Загрузка в Qdrant
    upload_to_qdrant(embeddings, chunks)

    print("✅ Обработка завершена.")
    return {
        "chunks_count": len(chunks),
        "embedding_dim": len(embeddings[0]) if embeddings else 0
    }
