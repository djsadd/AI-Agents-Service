from .model import embedding_model
from typing import List


def get_embeddings(text_chunks: List[str]) -> List[List[float]]:
    return embedding_model.encode(
        text_chunks,
        normalize_embeddings=True,
        show_progress_bar=True
    )
