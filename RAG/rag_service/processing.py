# processing.py

from services.utils.extract import extract_text
from services.utils.splitter import split_text
from services.embeddings.encode import get_embeddings
from services.qdrant.uploader import upload_to_qdrant
from services.document_api_client.api_services import create_embedding, create_chunks


def process_document(file_path, request):
    print(f"📄 Обработка документа: {file_path}")

    # 1. Извлечение текста
    text = extract_text(file_path)
    if not text.strip():
        raise ValueError("Извлечён пустой текст")

    # 2. Разделение на чанки
    chunks = split_text(text)
    chunk_objects = []
    for idx, chunk_text in enumerate(chunks):
        chunk_objects.append(create_chunks(document_id=request.POST.get("file_id"), text=chunk_text, chunk_index=idx))
    print(chunk_objects)
    print(chunk_objects[0])

    # 3. Эмбеддинги
    embeddings = get_embeddings(chunks)
    for chunk, vector in zip(chunk_objects, embeddings):
        create_embedding(vector=vector, chunk_id=chunk["id"])

    # 4. Загрузка в Qdrant
    upload_to_qdrant(embeddings, chunks, request.POST.get("file_id"), request.POST.get("project_id"))

    print("✅ Обработка завершена.")
    return {
        "chunks_count": len(chunks),
        "embedding_dim": len(embeddings[0]) if embeddings else 0
    }

