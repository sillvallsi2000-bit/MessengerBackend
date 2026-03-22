from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import ValidationError
from channels.db import database_sync_to_async
from apps.user.models import UserModel


@database_sync_to_async
def get_user_by_id(user_id):
    user = UserModel.objects.get(id=user_id)
    return user


class AuthMiddleware(BaseMiddleware):
    def validate_token(self, token):
        try:
            token = AccessToken(token)
            return token.get("user_id")

        except:
            raise ValidationError("token not valid")

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope.get("query_string").decode())
        token = query_string.get("token")[0]

        user_id = self.validate_token(token)
        user = await get_user_by_id(user_id=user_id)

        scope["user"] = user

        return await super().__call__(scope, receive, send)
