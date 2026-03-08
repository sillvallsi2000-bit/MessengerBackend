from django.urls import path
from .views import (
    ListCreateDirectChatAPI,
    ListCreateGroupAPI,
    ListCreateGroupAPI,
    ListCreateChannelAPI,
    CreateMembersAPI,
    ListofMembersAPI,
)

urlpatterns = [
    path("create_direct_chat/", ListCreateDirectChatAPI.as_view()),
    path("list_direct_chat/", ListCreateDirectChatAPI.as_view()),
    path("create_group/", ListCreateGroupAPI.as_view()),
    path("get_group/", ListCreateGroupAPI.as_view()),
    path("add_members/", CreateMembersAPI.as_view()),
    path("get_members/<int:chat_id>/", ListofMembersAPI.as_view()),
    path("create_channel/", ListCreateChannelAPI.as_view()),
    path("get_channel/", ListCreateChannelAPI.as_view()),
]
