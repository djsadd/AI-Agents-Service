import uuid
import requests
from .client import QDRANT_URL, COLLECTION_NAME, ensure_qdrant_collection

def upload_to_qdrant(embeddings, texts, file_id):
    ensure_qdrant_collection()
    url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points"

    points = []
    for vector, text in zip(embeddings, texts):
        points.append({
            "id": str(uuid.uuid4()),
            "vector": vector.tolist(),
            "payload": {
                "text": text,
                "file_id": file_id
            }
        })

    try:
        response = requests.put(url, json={"points": points})
        response.raise_for_status()
        print(f"✅ Загружено {len(points)} точек в Qdrant.")
    except Exception as e:
        print(f"❌ Ошибка при загрузке в Qdrant: {e}")
