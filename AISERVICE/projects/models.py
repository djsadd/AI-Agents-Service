from django.db import models
from users.models import User
# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Integration(models.Model):
    INTEGRATION_TYPES = [
        ('telegram', 'Telegram'),
        ('WhatsApp', 'WhatsApp'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="integrations")
    integration_type = models.CharField(max_length=50, choices=INTEGRATION_TYPES)
    config = models.JSONField(default=dict)  # сюда можно класть токены, ID и т.п.
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.integration_type} for {self.project}"
