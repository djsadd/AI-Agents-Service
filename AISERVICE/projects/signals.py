from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Integration
from .utils import update_telegram_webhook


@receiver(post_save, sender=Integration)
def integration_post_save_handler(sender, instance, created, **kwargs):
    update_telegram_webhook(instance)
