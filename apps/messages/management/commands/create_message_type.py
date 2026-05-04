from django.core.management.base import BaseCommand

from apps.messages.models import MessagesTypeModel
from core.enum.enum import MessageTypeChoices


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        types = [
            MessageTypeChoices.TEXT,
            MessageTypeChoices.IMAGE,
            MessageTypeChoices.FILE,
            MessageTypeChoices.VIDEO,
        ]
        for t in types:
            MessagesTypeModel.objects.get_or_create(name=t)
        self.stdout.write(self.style.SUCCESS("Chat types created successfully"))
