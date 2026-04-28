from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MessagesModel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import MessagesSerializer
from apps.chats.models import ChatMembersModel


@receiver(post_save, sender=MessagesModel)
def create_new_message(sender, instance, created, **kwargs):
    serializer = MessagesSerializer(instance)
    serializer = serializer.data
    if created:
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"chat_{instance.chat_id}", {"type": "sender", "message": serializer}
        )
