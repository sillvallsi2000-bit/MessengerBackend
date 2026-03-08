from datetime import timedelta
from typing import Any

from django.utils import timezone
from rest_framework.request import HttpRequest
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.auth.models import UserDeviceModel
from apps.user.models import UserModel
from core.dataclass.dataclass import DevicesDataclass, SessionDataclass, UserDataclass

from .session_service import SessionAccessToken


class OperationbyToken:

    def user_by_id(user_id: int) -> UserModel:
        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            raise ValidationError("")

        return user

    def update_token(
        user: UserDataclass, session: SessionDataclass
    ) -> tuple[RefreshToken, SessionAccessToken]:
        new_refresh = RefreshToken.for_user(user)
        new_access_token = SessionAccessToken()
        new_access_token["user_id"] = user.id
        new_access_token["session_id"] = session.id
        new_access_token["jti"] = new_refresh.access_token["jti"]
        new_access_token.set_exp()
        session.refresh_token = str(new_refresh)
        session.refresh_token_expire = timezone.now() + timedelta(days=7)
        session.last_activity = timezone.now()
        session.save()
        return new_refresh, new_access_token

    def validate_refresh_token(token) -> tuple[int, str, RefreshToken]:
        try:
            refresh_token = RefreshToken(token)

        except TokenError:
            raise ValidationError({"detail": "invalid token"})

        user_id: int = refresh_token.get("user_id")
        jti: str = refresh_token.get("jti")

        return user_id, jti, refresh_token


class OperationbyDevice:
    @staticmethod
    def get_ip_address(request: str | None):
        x_forward_for: str | None = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward_for:
            ip = x_forward_for.split(",")[0].strip()

        else:
            ip: str = request.META.get("REMOTE_ADDR")

        return ip

    @staticmethod
    def get_or_create_device(
        user: UserDataclass, request: HttpRequest
    ) -> DevicesDataclass:
        try:
            device: UserDeviceModel = UserDeviceModel.objects.get(user=user)
        except UserDeviceModel.DoesNotExist:
            device = UserDeviceModel.objects.create(
                user=user,
                device_name=request.data.get("device_name"),
                device_model=request.data.get("device_model"),
                user_agent=request.META.get("HTTP_USER_AGENT"),
                ip_address=OperationbyDevice.get_ip_address(request),
                os=request.data.get("os"),
                device_type=request.data.get("device_type"),
            )

        else:
            device.last_login = timezone.now()
            device.save()

        return device
