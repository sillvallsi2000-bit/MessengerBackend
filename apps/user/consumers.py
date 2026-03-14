from djangochannelsrestframework.generics import GenericAsyncAPIConsumer


class UserConsumer(GenericAsyncAPIConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass


# authentification
# user(scope)
