from .model import model
from typing import List
from typing import List, Literal

def get_embeddings(texts: List[str], mode: Literal["query", "passage"] = "passage") -> List[List[float]]:
    """
    Возвращает список эмбеддингов для списка текстов через локальную модель e5-small-v2.
    В зависимости от mode добавляется префикс:
    - "query:" для пользовательских запросов
    - "passage:" для документов/чанков
    """
    if mode not in ("query", "passage"):
        raise ValueError("mode должен быть либо 'query', либо 'passage'")

    prefixed_texts = [f"{mode}: {text}" for text in texts]
    return model.encode(prefixed_texts, convert_to_numpy=True).tolist()
