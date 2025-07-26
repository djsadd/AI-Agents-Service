import requests

QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "my_collection"
VECTOR_SIZE = 384


def ensure_qdrant_collection():
    url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}"
    resp = requests.get(url)

    if resp.status_code == 200:
        print("ℹ️ Коллекция уже существует.")
        return
    elif resp.status_code != 404:
        print(f"❌ Ошибка при проверке коллекции: {resp.text}")
        return

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
