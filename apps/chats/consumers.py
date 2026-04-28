from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from .models import ChatModel
import json


class ChatConsumers(GenericAsyncAPIConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = f"chat_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def sender(self, event):
        await self.send(
            text_data=json.dumps({"type": "chat", "data": event["message"]})
        )
