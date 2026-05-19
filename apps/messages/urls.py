from django.urls import path

from .views import (
    CreateForwardMessageAPI,
    CreateMessageAPI,
    CreateReactionMessageAPI,
    ListAllMessageAPI,
    RetrieveUpdateDestroyMessageAPI,
    RetrieveUpdateReactionMessageAPI,
)

urlpatterns = [
    path("create_message/", CreateMessageAPI.as_view()),
    path("list_message/<int:chat_id>/", ListAllMessageAPI.as_view()),
    path("update_destroy_message/<int:pk>/", RetrieveUpdateDestroyMessageAPI.as_view()),
    path("create_forward/", CreateForwardMessageAPI.as_view()),
    path("create_reaction/", CreateReactionMessageAPI.as_view()),
    path(
        "update_reaction/<int:message_id>/", RetrieveUpdateReactionMessageAPI.as_view()
    ),
]
