import openai
from qdrant_client import QdrantClient
from django.conf import settings
# Установи свой OpenAI API ключ через переменную окружения или здесь:
openai.api_key = settings.OPENAI_API_KEY

client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "my_collection"


def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    response = openai.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding


def get_best_match(question: str):
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
