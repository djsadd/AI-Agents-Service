from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from django.conf import settings
from .model import model
# Загружаем локальную модель один раз

# Настройки Qdrant
client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "rag_chunks"
from .encode import get_embeddings
from qdrant_client.http import models as rest

def get_best_match(question: str, project_id: int):
    vector = get_embeddings([question], mode="query")[0]  # ВАЖНО: берем [0]

    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,  # не список списков, а один список чисел
        limit=3,
        query_filter=rest.Filter(
            must=[
                rest.FieldCondition(
                    key="project_id",
                    match=rest.MatchValue(value=project_id)
                )
            ]
        ),
        with_payload=True
    )

    return hits[0].payload if hits else None
