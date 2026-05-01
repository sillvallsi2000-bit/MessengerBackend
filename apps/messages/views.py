from django.utils.timezone import now
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
)
from rest_framework.response import Response

from apps.chats.models import ChatModel

from .models import MessagesModel
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
        chat = ChatModel.objects.filter(id=message.chat_id).update(
            last_activity=now(), last_message_id=message.id
        )

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
