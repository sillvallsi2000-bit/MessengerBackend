from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .models import ChatModel, ChatMembersModel
from .serializers import (
    ChatDirectSerializer,
    ChatGroupSerializer,
    ChatChannelSerializer,
    AddMemberSerializer,
    ChatMembersSerializer,
)
from rest_framework.exceptions import PermissionDenied
from core.enum.enum import ChatTypesChoice
from django.shortcuts import get_object_or_404


class ListCreateDirectChatAPI(ListCreateAPIView):
    serializer_class = ChatDirectSerializer
    queryset = ChatModel.objects.all()
    permission_classes = [IsAuthenticated]


class ListCreateGroupAPI(ListCreateAPIView):
    serializer_class = ChatGroupSerializer
    queryset = ChatModel.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatModel.objects.filter(member__user=user).distinct()


class ListCreateChannelAPI(ListCreateAPIView):
    serializer_class = ChatChannelSerializer
    queryset = ChatModel.objects.all()

    def get_queryset(self):
        return ChatModel.objects.filter(chat_type=ChatTypesChoice.CHANNEL)


class CreateMembersAPI(CreateAPIView):
    serializer_class = AddMemberSerializer


class ListofMembersAPI(ListAPIView):
    serializer_class = ChatMembersSerializer
    queryset = ChatMembersModel.objects.all()

    def get_queryset(self):
        chat_id = self.kwargs["chat_id"]
        return ChatMembersModel.objects.filter(chat_id=chat_id)


# class RetrieveUpdateRoleAPI(RetrieveUpdateAPIView):
#     serializer_class = ChangeRoleSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         chat_id = self.kwargs["chat_id"]
#         target_user_id = self.kwargs["target_user_id"]

#         return get_object_or_404(
#             ChatMembersModel, chat_id=chat_id, user_id=target_user_id
#         )
