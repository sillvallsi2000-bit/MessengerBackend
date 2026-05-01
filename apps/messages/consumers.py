import json

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer


class MessageConsumers(GenericAsyncAPIConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.group_name = f"chat_{self.chat_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def sender(self, event):
        await self.send(
            text_data=json.dumps({"type": "message", "data": event["message"]})
        )
