from django.urls import path
from .views import (
    ListCreateDirectChatAPI,
    CreateGroupAPI,
    CreateMembersAPI,
    AddRoleChatAPI,
    CreateChannelAPI,
    DestroyMemberAPI,
    DestroyMemberRoleAPI,
    GetMeInfoAPI,
    BanMemberAPI,
    UpdateMembersAPI,
    UpdateChatSettingsAPI,
    UpdateGroupSettingsAPI,
    InviteMemberAPI,
    JoinToChatAPI,
    
)

# fmt: off

urlpatterns = [
    path("create_direct_chat/", ListCreateDirectChatAPI.as_view()),
    path("create_group/", CreateGroupAPI.as_view()),
    path("create_channel/", CreateChannelAPI.as_view()),
    path("list_chat/", ListCreateDirectChatAPI.as_view()),
    path("get_me_info/<int:chat_id>/", GetMeInfoAPI.as_view()),
    path("update_settings/chat/<int:chat_id>/", UpdateChatSettingsAPI.as_view()),
    path("update_settings_group/chat/<int:chat_id>/", UpdateGroupSettingsAPI.as_view())


    ,

    # change


    path("add_member/<int:chat_id>/", CreateMembersAPI.as_view()),
    path(
        "delete_member/<int:target_id>/chat/<int:chat_id>/", DestroyMemberAPI.as_view()
    ),
    path(
        "update_member/<int:chat_id>/", UpdateMembersAPI.as_view()
    ),
    # change_ two step


    path(
        "chats/<int:pk>/add_role/",
        AddRoleChatAPI.as_view(),
    ),
    path(
        "delete_member_role/<int:target_id>/chat/<int:chat_id>/",
        DestroyMemberRoleAPI.as_view(),
    ),
    path(
        "ban_user/<int:chat_id>/chat/",
        BanMemberAPI.as_view(),
    ),
    path(
        "invite_user/<int:chat_id>/",
        InviteMemberAPI.as_view(),
    ),
    path(
        "join_to_chat/",
        JoinToChatAPI.as_view(),
    ),


]

# fmt: on
