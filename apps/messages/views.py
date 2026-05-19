from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.chats.models import ChatModel

from .models import MessageMetadataModel, MessageReactionModel, MessagesModel
from .serializers import (
    CreateForwardMessageSerializer,
    CreateMessageSerializer,
    MessageReactionSerializer,
    MessageRetrieveUpdateDestroySerializer,
    MessagesSerializer,
)


class CreateMessageAPI(CreateAPIView):
    serializer_class = CreateMessageSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(
            data=data, context={"sender": self.request.user}
        )
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        files = self.request.FILES.getlist("files")
        for file in files:
            MessageMetadataModel.objects.bulk_create(
                [
                    MessageMetadataModel(
                        message=message,
                        file_url=default_storage.save(f"uploads/{file.name}", file),
                        file_size=file.size,
                        file_name=file.name,
                    )
                ]
            )

        ChatModel.objects.filter(id=message.chat_id).update(
            last_activity=now(), last_message_id=message.id
        )
        message.refresh_from_db()

        message_data = MessagesSerializer(
            message, context={"request": self.request}
        ).data

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{message.chat_id}", {"type": "sender", "message": dict(message_data)}
        )

        return Response(message_data)


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


class RetrieveUpdateDestroyMessageAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = MessageRetrieveUpdateDestroySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MessagesModel.objects.filter(sender=self.request.user, is_delited=False)

    def perform_destroy(self, instance):
        instance.is_delited = True
        instance.save(update_fields=["is_delited"])


class CreateForwardMessageAPI(CreateAPIView):
    serializer_class = CreateForwardMessageSerializer
    permission_classes = [IsAuthenticated]


class CreateReactionMessageAPI(CreateAPIView):
    serializer_class = MessageReactionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = self.get_serializer(data=data, context={"user": self.request.user})
        serializer.is_valid(raise_exception=True)
        reaction = serializer.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{reaction.message.chat_id}",
            {
                "type": "sender",
                "message": {
                    "type": "reaction",
                    "message_id": reaction.message.id,
                    "emoji": reaction.type,
                    "user_id": self.request.user.id,
                },
            },
        )
        return Response(serializer.data)


class RetrieveUpdateReactionMessageAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = MessageReactionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "message_id"

    def get_object(self):
        return get_object_or_404(
            MessageReactionModel,
            user=self.request.user,
            message=self.kwargs["message_id"],
        )
