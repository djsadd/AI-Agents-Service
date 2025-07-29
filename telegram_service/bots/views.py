from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# Create your views here.


@csrf_exempt
def telegram_webhook(request, token):
    if request.method == 'POST':
        payload = json.loads(request.body)
        print(f"📩 New update for bot {token}: {payload}")
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "only POST allowed"}, status=405)
