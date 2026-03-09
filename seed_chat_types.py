from django.core.management.base import BaseCommand
from apps.chat.models import ChatTypesModel
from core.enum.enum import ChatTypesChoice

class Command(BaseCommand):
  def handle(self,*args, **kwargs ):
    types = [ChatTypesChoice.DIRECT, ChatTypesChoice.GROUP, ChatTypesChoice.CHANNEL]
    for t in types:
      ChatTypesModel.objects.get_or_create(name = t)
    self.stdout.write(self.style.SUCCESS("Chat types created successfully"))
