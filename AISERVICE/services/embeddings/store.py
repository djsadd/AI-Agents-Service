from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from django.conf import settings

# Загружаем локальную модель один раз
model = SentenceTransformer("intfloat/multilingual-e5-small")

# Настройки Qdrant
client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "my_collection"


def get_embedding(text: str) -> list[float]:
    """
    Получить эмбеддинг для текста с помощью локальной модели e5-small-v2.
    Важно: добавь префикс "query:".
    """
    embedding = model.encode(f"query: {text}", convert_to_numpy=True)
    return embedding.tolist()


def get_best_match(question: str):
    """
    Выполняет поиск ближайшего совпадения в Qdrant по смыслу.
    """
    vector = get_embedding(question)

    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=1
    )

    if hits:
        return hits[0].payload  # например, {"text": "...", "file_id": "..."}
    else:
        return "❌ No results found."
