from channels.routing import URLRouter

from django.urls import path
from apps.user.routing import websocket_urlpatterns as user_router
from apps.user.consumers import UserConsumer

websocket_urlpatterns = [
    path("ws/user/", as_asgi()),
]
