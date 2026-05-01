from django.db.models.signals import post_save
from django.dispatch import receiver

from core.services.chat_service import getUsersFromChat

from .models import ChatMembersModel


@receiver(post_save, sender=ChatMembersModel)
def create_chat(sender, instance, created, **kwargs):
    if not created:
        return
    getUsersFromChat(instance.chat)


# verificate instance owner
