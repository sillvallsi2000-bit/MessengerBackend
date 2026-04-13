from django.urls import path

from .views import (
    ListCreateBlockUserAPI,
    ListCreateContactUserAPI,
    RetrieveUpdateContactAPI,
    UserCreateAPI,
    UserPrivatyAPI,
    UserProfileAPI,
    UserSettingsAPI,
    GetUserAPI,
    SearchUserByName,
    SearchContactsUserByName,
)

urlpatterns = [
    path("create_user/", UserCreateAPI.as_view()),
    path("get_profile/", UserProfileAPI.as_view()),
    path("get_me/", GetUserAPI.as_view()),
    path("update_profile/", UserProfileAPI.as_view()),
    path("get_user_settings/", UserSettingsAPI.as_view()),
    path("update_user_settings/", UserSettingsAPI.as_view()),
    path("get_user_privaty/", UserPrivatyAPI.as_view()),
    path("update_user_privaty/", UserPrivatyAPI.as_view()),
    path("block_user/", ListCreateBlockUserAPI.as_view()),
    path("list_block_user/", ListCreateBlockUserAPI.as_view()),
    path("create_contact/", ListCreateContactUserAPI.as_view()),
    path("list_contacts/", ListCreateContactUserAPI.as_view()),
    path("update_contact/<int:pk>/", RetrieveUpdateContactAPI.as_view()),
    path("get_contact/<int:pk>/", RetrieveUpdateContactAPI.as_view()),
    path("search_by_username/<str:username>/", SearchUserByName.as_view()),
    path("search_by_contacts/<str:username>/", SearchContactsUserByName.as_view()),
]
