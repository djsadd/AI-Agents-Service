from django.shortcuts import render

# Create your views here.


from groq import Groq
import os
from django.conf import settings


client = Groq(api_key=settings.GROQ_API_KEY)


def ask_groq(context, prompt) -> str:
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": '''
                    Ты — интеллектуальный помощник(ассистент) в приёмной комиссии университета
                     Туран-Астана. на 2025-2026 уч.год.
                     Ответь строго на основе приведённого контекста. Если ответа нет, скажи: "Информация отсутствует".
                     
                    '''
                },
                {
                    "role": "user",
                    "content": f"контекст:{context}, промпт{prompt}", # передать вопрос пользователя
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Произошла ошибка: {e}"