from django.shortcuts import render

# Create your views here.


from groq import Groq
import os
from django.conf import settings

from projects.models import Project
from services.embeddings.store import get_best_match
import requests

client = Groq(api_key=settings.GROQ_API_KEY)


def ask_question_view(request, project_pk):
    context = {}

    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            # best_match = get_best_match(question, project_pk)
            api_url = "http://localhost:8001/api/get_best_match/"
            data = {
                'question': question,
                'project_pk': project_pk,
            }
            project = Project.objects.get(pk=project_pk)
            response = requests.post(api_url, data=data)
            json_data = response.json()

            best_match = json_data.get("result")

            if best_match and "text" in best_match:
                retrieved_context = best_match["text"]
                # ❗ Вот здесь вызывается твоя функция
                llm_answer = ask_groq(retrieved_context, question, project.system_text)

                context['question'] = question
                context['answer'] = llm_answer
                context['retrieved_context'] = retrieved_context
                context['source'] = best_match.get('file_id', 'N/A')  # если хочешь
                # print(context['source'])
            else:
                context['answer'] = "❌ Ничего не найдено в базе знаний."

    return render(request, 'fileprocessing/ask.html', context)


def ask_question_telegram_view(request, question, project_pk, system_text):
    context = {}
    if question:
        # best_match = get_best_match(question, project_pk)
        api_url = "http://localhost:8001/api/get_best_match/"
        data = {
            'question': question,
            'project_pk': project_pk,
        }
        response = requests.post(api_url, data=data)
        json_data = response.json()

        best_match = json_data.get("result")

        if best_match and "text" in best_match:
            retrieved_context = best_match["text"]
            # ❗ Вот здесь вызывается твоя функция
            llm_answer = ask_groq(retrieved_context, question, system_text)

            context['question'] = question
            context['answer'] = llm_answer
            context['retrieved_context'] = retrieved_context
            context['source'] = best_match.get('file_id', 'N/A')  # если хочешь
        else:
            context['answer'] = "❌ Ничего не найдено в базе знаний."
        return context

    return "Задайте вопрос"


def ask_groq(context, prompt, system_text) -> str:
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": f"{system_text}"
                },
                {
                    "role": "user",
                    "content": f"Данные я тебе передаю, на основе них построй ответ:{context},"
                               f"Вопрос пользователя: {prompt}",
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Произошла ошибка: {e}"