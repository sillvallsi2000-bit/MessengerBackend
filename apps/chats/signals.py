from .models import ChatModel
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import ChatSerializer
from django.db.models.signals import post_save
from .models import ChatMembersModel
from core.services.chat_service import getUsersFromChat


@receiver(post_save, sender=ChatMembersModel)
def create_chat(sender, instance, created, **kwargs):
    if not created:
        return
    getUsersFromChat(instance.chat)


# verificate instance owner
