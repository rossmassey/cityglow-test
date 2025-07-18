from django.urls import path

from api.calls.views import HelloView
from api.calls.views.hello_view import FirestoreTestView

app_name = 'calls'

urlpatterns = [
    path('hello/', HelloView.as_view(), name='hello'),
    path('firestore/', FirestoreTestView.as_view(), name='firestore-test'),
]
