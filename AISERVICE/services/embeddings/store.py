from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import SearchRequest, Filter, PointStruct
from qdrant_client.models import Distance, VectorParams
import numpy as np

# Загружаем модель (если используется SentenceTransformer)
embedding_model = SentenceTransformer("BAAI/bge-base-en-v1.5")

# Подключаемся к Qdrant
client = QdrantClient(host="localhost", port=6333)  # проверь порт!

# Название коллекции, которую ты заранее создал
COLLECTION_NAME = "my_collection"


def get_embedding(text: str) -> list[float]:
    embedding = embedding_model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def get_best_match(question: str):
    vector = get_embedding(question)

    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=1
    )

    if hits:
        return hits[0].payload  # или hits[0].payload["text"], зависит от структуры
    else:
        return "❌ No results found."
