from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from projects.models import Integration, Project
from llm.views import ask_question_telegram_view
# Create your views here.

import requests


def send_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=data)
    print(f"📤 Send message response: {response.status_code}, {response.text}")


@csrf_exempt
def telegram_webhook(request, token):
    if request.method != 'POST':
        return JsonResponse({"status": "only POST allowed"}, status=405)

    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    print(f"📩 Incoming webhook for token: {token}")

    # Найти Integration по типу и config["bot_token"]
    integration = Integration.objects.filter(
        integration_type='telegram',
        config__bot_token=token,
        enabled=True
    ).first()

    if not integration:
        return JsonResponse({"error": "Integration not found"}, status=404)

    print(f"✅ Found integration for project: {integration.project.name}")

    # (Опционально) Обрабатываем сообщение
    message = payload.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text")
    if text:
        if request.method == 'POST':
            payload = json.loads(request.body)
            print(f"📩 New update for bot {token}: {payload}")

            # Получаем текст сообщения
            message = payload.get("message") or payload.get("edited_message")
            if message:
                chat_id = message["chat"]["id"]
                text = message.get("text", "")

                print(f"👤 Пользователь: {chat_id}")
                print(f"💬 Вопрос: {text}")
        answer = ask_question_telegram_view(request, text, integration.project.pk)
        send_message(token, chat_id, answer["answer"])

    return JsonResponse({"status": "ok"})
