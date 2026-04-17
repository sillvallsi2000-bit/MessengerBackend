from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from apps.user.models import StatusUserModel
from channels.db import database_sync_to_async
import json
from rest_framework.exceptions import ValidationError


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

    # async def send_user(self, event):
    #     await self.send_json(event)

    # @database_sync_to_async
    # def user_is_online(self):
    #     self.user.status.is_online = True
    #     self.user.status.save()

    # @database_sync_to_async
    # def user_is_ofline(self):
    #     self.user.status.is_online = False
    #     self.user.status.save()
