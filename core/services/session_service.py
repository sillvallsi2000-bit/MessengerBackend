from datetime import timedelta
from typing import Any, Optional, Tuple

from django.utils import timezone
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken

from apps.auth.models import UserSessionModel
from core.dataclass.dataclass import DevicesDataclass, SessionDataclass, UserDataclass
from core.enum.enum import UserSessionStatus

from rest_framework.request import HttpRequest
from core.dataclass.dataclass import UserDataclass, SessionDataclass


class SessionAccessToken(AccessToken):
    def __init__(self, token=None, verify=True, session_id=None):
        super().__init__(
            token,
            verify,
        )
        if session_id:
            self.session_id = str(session_id)


class JwtSessionAuth(JWTAuthentication):
    def authenticate(self, request: HttpRequest):
        data = super().authenticate(request)
        if not data:
            return None
        user, token = data
        session_id: str = token.get("session_id")
        if not session_id:
            raise ValidationError({"detail": "invalid token"})
        try:
            session: UserSessionModel = UserSessionModel.objects.get(
                id=session_id, user=user, status=UserSessionStatus.ACTIVE
            )

        except UserSessionModel.DoesNotExist:
            raise ValidationError({"detail": "session not active"})

        request.session = session
        return user, token


class OperationbySession:
    def create_session(
        user: UserDataclass, device: DevicesDataclass, data: dict[str, Any]
    ) -> SessionDataclass:
        session: SessionDataclass = UserSessionModel.objects.create(
            user=user,
            device=device,
            refresh_token=data["refresh"],
            refresh_token_expire=timezone.now() + timedelta(days=7),
            status=UserSessionStatus.ACTIVE,
            last_activity=timezone.now(),
        )
        session.save()
        return session

    def get_active_session(user_id: int, refresh) -> SessionDataclass:
        try:
            session: SessionDataclass = UserSessionModel.objects.get(
                user_id=user_id, refresh_token=refresh, status=UserSessionStatus.ACTIVE
            )

        except UserSessionModel.DoesNotExist:
            raise ValidationError({"detail": "session invalid"})

        if session.refresh_token_expire < timezone.now():
            session.status = UserSessionStatus.EXPIRED
            session.save()
            raise ValidationError({"detail": "token expired"})

        return session

    def logout_session(session: SessionDataclass) -> None:
        session.status = UserSessionStatus.LOGOUT
        session.last_activity = timezone.now()
        session.save()
