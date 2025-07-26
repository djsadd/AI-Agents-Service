from .model import model
from typing import List
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def get_embeddings(texts: List[str], model=model):
    """
    Возвращает список эмбеддингов для списка текстов через OpenAI API.
    """
    response = openai.Embedding.create(
        input=texts,
        model=model
    )
    return [item.embedding for item in response.data]
