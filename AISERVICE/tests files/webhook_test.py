import requests

def check_telegram_webhook(bot_token):
    url = f"https://api.telegram.org/bot{bot_token}/getWebhookInfo"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("ℹ️ Webhook info:")
        print(data)
    else:
        print(f"❌ Ошибка: {response.status_code}, {response.text}")

check_telegram_webhook("7453926084:AAH4THVP7WpE9EeqIjDUUrPzoQ3Glj4DF8o")
