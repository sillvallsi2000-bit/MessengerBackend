from django.urls import path
from .consumers import ChatConsumers

websocket_urlpatterns = [path("ws/chat/", ChatConsumers.as_asgi())]
