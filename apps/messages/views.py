from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.files.storage import default_storage
from django.utils.timezone import now
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
)
from rest_framework.response import Response

from apps.chats.models import ChatModel

from .models import MessageMetadataModel, MessagesModel
from .serializers import (
    CreateMessageSerializer,
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

        audio_file = self.request.FILES.get("audio")
        if audio_file:
            file_path = default_storage.save(f"audio/{audio_file.name}", audio_file)
            MessageMetadataModel.objects.create(
                message=message,
                file_url=file_path,
                file_size=audio_file.size,
                file_name=audio_file.name,
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
