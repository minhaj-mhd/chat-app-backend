from django.urls import path
from .consumers import PersonalClassConsumer
websocket_urlpatterns = [
    path('ws/chat/<int:id>/',PersonalClassConsumer.as_asgi())
]