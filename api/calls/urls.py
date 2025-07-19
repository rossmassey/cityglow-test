from django.urls import path

from api.calls.views import VapiWebhookView, ElevenLabsWebhookView, ElevenLabsStreamView

app_name = 'calls'

urlpatterns = [
    path('vapi-webhook/', VapiWebhookView.as_view(), name='vapi-webhook'),
    path('elevenlabs-webhook/', ElevenLabsWebhookView.as_view(), name='elevenlabs-webhook'),
    path('<str:conversation_id>/elevenlabs_stream/', ElevenLabsStreamView.as_view(), name='elevenlabs-stream'),
]
