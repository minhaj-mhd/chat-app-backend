from django.urls import path
from .consumers import PersonalClassConsumer
websocket_urlpatterns = [
    path('ws/chat/',PersonalClassConsumer.as_asgi())
]