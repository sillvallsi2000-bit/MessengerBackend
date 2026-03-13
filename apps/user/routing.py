from django.urls import path
from .consumers import UserConsumer

websocket_urlpatterns = [path("user/", UserConsumer.as_asgi())]
