from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from apps.user.models import StatusUserModel
from channels.db import database_sync_to_async
import json
from rest_framework.exceptions import ValidationError


class UserConsumer(GenericAsyncAPIConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.group_name = "user_status"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "send_user", "user_id": self.user.id, "status": True},
        )
        await self.accept()
        await self.user_is_online()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.user_is_ofline()
        await self.channel_layer.group_send(
            self.group_name,
            {"type": "send_user", "user_id": self.user.id, "status": False},
        )

    async def send_user(self, event):
        await self.send_json(event)

    @database_sync_to_async
    def user_is_online(self):
        self.user.status.is_online = True
        self.user.status.save()

    @database_sync_to_async
    def user_is_ofline(self):
        self.user.status.is_online = False
        self.user.status.save()
