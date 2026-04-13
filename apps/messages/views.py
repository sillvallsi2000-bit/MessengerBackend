from django.shortcuts import render
from .serializers import (
    ModelSerializer,
    MessageForwardSerializer,
    MessageEditSerializer,
    MessageHashtagSerializer,
    MessageLinkSerializer,
    MessageMetadataSerializer,
    MessageReactionSerializer,
    MessageReplaysSerializer,
    MessagesSerializer,
    MessageStatusSerializer,
    MessagesTypeSerializer,
    CreateMessageSerializer,
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    ListAPIView,
)

from rest_framework.response import Response

from .models import MessagesModel
from apps.chats.models import ChatModel, ChatMembersModel

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied


class CreateMessageAPI(CreateAPIView):
    serializer_class = CreateMessageSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        user = self.request.user
        serializer = self.get_serializer(
            data=data, context={"sender": self.request.user}
        )
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        return Response(MessagesSerializer(message).data)


class ListAllMessageAPI(ListAPIView):
    serializer_class = MessagesSerializer

    def get_queryset(self):
        user = self.request.user
        chat_id = self.kwargs.get("chat_id")

        chat = ChatModel.objects.filter(id=chat_id).first()

        if not chat:
            raise PermissionDenied("Chat not found")

        if chat.owner != user:
            pass

        return MessagesModel.objects.filter(chat=chat)

    # create chat front
    # mediadata
