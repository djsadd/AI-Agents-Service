from django import forms
from .models import Integration


class BaseIntegrationForm(forms.ModelForm):
    class Meta:
        model = Integration
        fields = ['enabled']  # общие поля


class TelegramIntegrationForm(BaseIntegrationForm):
    bot_token = forms.CharField(label="Bot Token")

    def clean(self):
        cleaned = super().clean()
        cleaned['config'] = {
            'bot_token': cleaned.get('bot_token'),
        }
        return cleaned

    def save(self, commit=True):
        self.instance.integration_type = 'telegram'
        self.instance.config = self.cleaned_data['config']
        return super().save(commit)


class WhatsAppIntegrationForm(BaseIntegrationForm):
    phone_number = forms.CharField(label="Номер телефона")
    api_key = forms.CharField(label="API ключ")

    def clean(self):
        cleaned = super().clean()
        cleaned['config'] = {
            'phone_number': cleaned.get('phone_number'),
            'api_key': cleaned.get('api_key'),
        }
        return cleaned

    def save(self, commit=True):
        self.instance.integration_type = 'WhatsApp'
        self.instance.config = self.cleaned_data['config']
        return super().save(commit)
