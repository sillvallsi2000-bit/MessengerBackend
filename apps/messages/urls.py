from django.urls import path
from .views import CreateMessageAPI, ListAllMessageAPI


urlpatterns = [
    path("create_message/", CreateMessageAPI.as_view()),
    path("list_message/<int:chat_id>/", ListAllMessageAPI.as_view()),
]
