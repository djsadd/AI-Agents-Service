from .model import model
from typing import List


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Возвращает список эмбеддингов для списка текстов через локальную модель e5-small-v2.
    Важно: добавляй префиксы "query:" или "passage:" в зависимости от задачи.
    """
    return model.encode(texts, convert_to_numpy=True).tolist()
