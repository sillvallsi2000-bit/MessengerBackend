from django.urls import path
from .consumers import MessageConsumers

websocket_urlpatterns = [path("ws/chat/<int:chat_id>/", MessageConsumers.as_asgi())]
