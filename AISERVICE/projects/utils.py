import requests
import logging
from .models import Integration

logger = logging.getLogger(__name__)


def update_telegram_webhook(instance: Integration):
    if instance.integration_type != 'telegram':
        logger.info("🔁 Пропущено: не telegram-интеграция")
        return

    bot_token = instance.config.get('bot_token')
    if not bot_token:
        logger.warning("⛔ Не найден bot_token в config")
        return

    SERVICE_BASE_URL = 'https://8784e0b036d5.ngrok-free.app'  # заменить
    webhook_url = f"{SERVICE_BASE_URL}/webhook/{bot_token}/"

    try:
        check = requests.get(f"https://api.telegram.org/bot{bot_token}/getWebhookInfo", timeout=10)
        current_url = check.json().get("result", {}).get("url", "")

        if current_url == webhook_url:
            logger.info(f"✅ Webhook уже установлен: {webhook_url}")
        else:
            response = requests.post(
                f"https://api.telegram.org/bot{bot_token}/setWebhook",
                json={"url": webhook_url},
                timeout=10
            )

            if response.status_code == 200:
                logger.info(f"✅ Установлен новый webhook: {webhook_url}")
            else:
                logger.error(f"❌ Ошибка установки webhook: {response.status_code} — {response.text}")
                return

        if instance.config.get('webhook_url') != webhook_url:
            new_config = instance.config.copy()
            new_config['webhook_url'] = webhook_url
            Integration.objects.filter(pk=instance.pk).update(config=new_config)
            logger.info("📝 Config обновлён с webhook_url")

    except Exception as e:
        logger.exception(f"💥 Ошибка при работе с Telegram API: {e}")
