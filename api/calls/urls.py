from django.urls import path

from api.calls.views import VapiWebhookView, ElevenLabsWebhookView

app_name = 'calls'

urlpatterns = [
    path('vapi-webhook/', VapiWebhookView.as_view(), name='vapi-webhook'),
    path('elevenlabs-webhook/', ElevenLabsWebhookView.as_view(), name='elevenlabs-webhook'),
]
