from django.urls import path
from api.calls.views import HelloView

app_name = 'calls'

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
]
