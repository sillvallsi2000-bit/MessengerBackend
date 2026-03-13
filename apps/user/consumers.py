from djangochannelsrestframework.generics import GenericAsyncAPIConsumer


class UserConsumer(GenericAsyncAPIConsumer):
    async def connect(self):
        await

    async def disconnect(self, code):
        pass
