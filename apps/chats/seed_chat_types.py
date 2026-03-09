from django.core.management.base import BaseCommand
from apps.chat.models import ChatTypeModel

class Command(BaseCommand):
  def handle(self,*args, **kwargs ):
    types =["DIRECT", "GROUP", "CHANNEL"]
    for t in types:
      ChatTypeModel.objects.get_or_create(name = t)
    self.stdout.write(self.style.SUCCESS("Chat types created successfully"))
  

