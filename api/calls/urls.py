from django.urls import path

from api.calls.views import ElevenLabsWebhookView, ElevenLabsStreamView, CallsListView

app_name = 'calls'

urlpatterns = [
    path('elevenlabs-webhook/', ElevenLabsWebhookView.as_view(), name='elevenlabs-webhook'),
    path('elevenlabs_stream/<str:conversation_id>/', ElevenLabsStreamView.as_view(), name='elevenlabs-stream'),
    path('list/', CallsListView.as_view(), name='calls-list'),
]
