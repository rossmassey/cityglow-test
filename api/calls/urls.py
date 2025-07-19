from django.urls import path

from api.calls.views import VapiWebhookView, ElevenLabsWebhookView, ElevenLabsStreamView

app_name = 'calls'

urlpatterns = [
    path('vapi-webhook/', VapiWebhookView.as_view(), name='vapi-webhook'),
    path('elevenlabs-webhook/', ElevenLabsWebhookView.as_view(), name='elevenlabs-webhook'),
    path('elevenlabs_stream/<str:conversation_id>/', ElevenLabsStreamView.as_view(), name='elevenlabs-stream'),
]
