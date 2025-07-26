import uuid
import requests
from .client import QDRANT_URL, COLLECTION_NAME, ensure_qdrant_collection


def upload_to_qdrant(embeddings, texts, file_id, project_id):
    if len(embeddings) != len(texts):
        raise ValueError(f"Длина embeddings ({len(embeddings)}) не равна длине texts ({len(texts)})")

    ensure_qdrant_collection()
    url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points"
    print("Embedding size example:", len(embeddings[0]))

    points = []
    for vector, text in zip(embeddings, texts):
        points.append({
            "id": str(uuid.uuid4()),
            "vector": vector,
            "payload": {
                "text": text,
                "file_id": file_id,
                "project_id": project_id
            }
        })

    try:
        response = requests.put(url, json={"points": points})
        response.raise_for_status()
        print(f"✅ Загружено {len(points)} точек в Qdrant.")
    except Exception as e:
        print(f"❌ Ошибка при загрузке в Qdrant: {e}")
