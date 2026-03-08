from typing import Any, Dict

from django.utils import timezone
from rest_framework import serializers
from rest_framework.request import HttpRequest
from rest_framework.serializers import ModelSerializer, Serializer, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.user.serializers import UserSerializer
from core.dataclass.dataclass import DevicesDataclass, SessionDataclass, UserDataclass
from core.services.auth_service import OperationbyDevice, OperationbyToken
from core.services.email_service import EmailService
from core.services.session_service import OperationbySession

from .models import CodeUserModel, UserDeviceModel, UserSessionModel


class SessionSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserSessionModel
        fields = (
            "id",
            "user",
            "device",
            "refresh_token",
            "refresh_token_expire",
            "ip_address",
            "status",
            "last_activity",
        )


class UserDeviceSerializer(ModelSerializer):
    class Meta:
        model = UserDeviceModel
        fields = (
            "id",
            "device_name",
            "device_model",
            "user_agent",
            "os",
            "is_active",
            "device_type",
            "last_login",
        )
        read_only_fields = (
            "id",
            "user_agent",
        )


class CodeSerialiser(ModelSerializer):
    class Meta:
        model = CodeUserModel
        fields = (
            "id",
            "user",
            "code",
            "verificated_at",
            "expired_at",
        )
        read_only_fields = (
            "id",
            "user",
            "verificated_at",
            "expired_at",
        )

    def validate(self, attrs: Dict[str, Any]):
        request: HttpRequest = self.context.get("request")
        user: UserDataclass = request.user
        if not user:
            raise ValidationError({"detail": "user is required"})
        code = attrs.get("code")
        try:
            code = CodeUserModel.objects.get(user=user, code=code)

        except CodeUserModel.DoesNotExist:
            raise ValidationError({"detail": "code doesn't exist"})

        attrs["code"] = code
        return attrs


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        request: HttpRequest = self.context.get("request")
        user: UserDataclass = self.user

        device: DevicesDataclass = OperationbyDevice.get_or_create_device(user, request)
        session: SessionDataclass = OperationbySession.create_session(
            user=user, device=device, data=data
        )
        refresh, access = OperationbyToken.update_token(user=user, session=session)
        return {"access": str(access), "refresh": str(refresh)}


class RefreshSerializer(Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        refresh_token: str = attrs.get("refresh")
        user_id, _, refresh_token = OperationbyToken.validate_refresh_token(
            refresh_token
        )
        session: SessionDataclass = OperationbySession.get_active_session(
            user_id=user_id, refresh=refresh_token
        )

        user: UserDataclass = OperationbyToken.user_by_id(user_id)

        refresh, access = OperationbyToken.update_token(user=user, session=session)
        return {"access": str(access), "refresh": str(refresh)}
