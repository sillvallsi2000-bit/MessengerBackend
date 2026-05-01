from apps.chats.routing import websocket_urlpatterns as chats_router
from apps.messages.routing import websocket_urlpatterns as message_router
from apps.user.routing import websocket_urlpatterns as user_router

websocket_urlpatterns = user_router + message_router + chats_router
