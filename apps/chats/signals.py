from .models import ChatModel
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .serializers import ChatSerializer
from django.db.models.signals import post_save
from .models import ChatMembersModel


@receiver(post_save, sender=ChatMembersModel)
def create_chat(sender, instance, created, **kwargs):
    print("ok")
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{instance.user_id}",
            {"type": "sender", f"message": f"chat create {instance.chat_id}"},
        )


# verificate instance owner
