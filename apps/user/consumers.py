from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from apps.user.models import StatusUserModel
from channels.db import database_sync_to_async
import json


class UserConsumer(GenericAsyncAPIConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        await self.user_is_online()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print(self.user)

        await self.accept()

    async def disconnect(self, code):
        await self.user_is_ofline()

    @database_sync_to_async
    def user_is_online(self):
        self.user.status.is_online = True
        self.user.status.save()

    @database_sync_to_async
    def user_is_ofline(self):
        self.user.status.is_online = False

        self.user.status.save()
