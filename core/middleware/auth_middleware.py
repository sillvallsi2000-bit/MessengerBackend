from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import ValidationError
from channels.db import database_sync_to_async
from apps.user.models import UserModel
from apps.auth.models import UserSessionModel
from core.enum.enum import UserSessionStatus
from channels.exceptions import DenyConnection
import json


@database_sync_to_async
def get_user_by_id(user_id):
    user = UserModel.objects.get(id=user_id)
    return user


@database_sync_to_async
def get_session(session_id):
    try:
        session: UserSessionModel = UserSessionModel.objects.get(
            id=session_id, status=UserSessionStatus.ACTIVE
        )
        print(session)
    except UserSessionModel.DoesNotExist:
        raise ValidationError({"detail": "session not active"})


class AuthMiddleware(BaseMiddleware):

    async def validate_token(self, token):
        try:
            token = AccessToken(token)

        except:
            raise ValidationError("token not valid")

        session_id: str = token.get("session_id")
        if not session_id:
            raise ValidationError("session not valid")
        await get_session(session_id)
        return token.get("user_id")

    async def __call__(self, scope, receive, send):
        try:
            query_string = parse_qs(scope.get("query_string").decode())
            token = query_string.get("token")[0]

            user_id = await self.validate_token(token)
            user = await get_user_by_id(user_id=user_id)

            scope["user"] = user

        except ValidationError as e:
            await send({"type": "websocket.accept"})
            await send(
                {"type": "websocket.send", "text": json.dumps({"error": e.detail})}
            )
            return

        return await super().__call__(scope, receive, send)

    # error
    # front
