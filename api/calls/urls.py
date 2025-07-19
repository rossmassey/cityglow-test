from django.urls import path

from api.calls.views import VapiWebhookView

app_name = 'calls'

urlpatterns = [
    path('vapi-webhook/', VapiWebhookView.as_view(), name='vapi-webhook'),
]
