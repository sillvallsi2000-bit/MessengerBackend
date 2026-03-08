from typing import Any, Dict

from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, ValidationError

from apps.user.models import ProfileUserModel
from core.dataclass.dataclass import (
    BlockUserDataclass,
    ContactUserDataclass,
    UserDataclass,
    UserProfileDataclass,
)
from core.services.email_service import EmailService

from .models import (
    BlockUserModel,
    ProfileUserModel,
    UserContactsModel,
    UserModel,
    UserPrivatyModel,
    UserSettingsModel,
)
from core.services.auth_service import OperationbyDevice, OperationbyToken
from core.services.email_service import EmailService
from core.services.session_service import OperationbySession
from rest_framework.request import HttpRequest


class UserProfileSerializer(ModelSerializer):

    class Meta:
        model = ProfileUserModel
        fields = (
            "id",
            "username",
            "birthday",
            "bio",
            "avatar",
            "name",
            "surname",
            "phone",
        )


class UserSettingsSerializer(ModelSerializer):
    class Meta:
        model = UserSettingsModel
        fields = (
            "id",
            "theme",
            "language",
            "notification_enable",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class UserPrivatySerializer(ModelSerializer):

    class Meta:
        model = UserPrivatyModel
        fields = (
            "id",
            "profile_photo_visible",
            "allow_message",
            "allow_calls",
            "forward_message",
            "show_phone_number",
            "profile_visible",
        )


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ("id", "email", "password", "is_active", "is_verificate")
        read_only_fields = ("is_active", "is_verificate")

    def create(self, validated_data):
        user: UserDataclass = UserModel.objects.create_user(**validated_data)
        EmailService.sendregistrcode(user)

        return user


class ContactsUserSerializers(ModelSerializer):
    class Meta:
        model = UserContactsModel
        fields = (
            "id",
            "user",
            "contact_user",
            "contact_name",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "user", "created_at", "updated_at")

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        request: Request = self.context.get("request")
        user: UserDataclass = request.user
        contact_user: ContactUserDataclass = attrs.get("contact_user")
        contact_name: str = attrs.get("contact_name")
        profile_user: UserProfileDataclass = ProfileUserModel.objects.get(user=user)

        if BlockUserModel.objects.filter(user=user, blocked_user=contact_user).first():
            raise ValidationError({"detail": " user is blocked"})

        if user == contact_user:
            raise ValidationError({"detail": "you can not add yourself in contact"})

        if UserContactsModel.objects.filter(
            user=user, contact_user=contact_user
        ).first():
            raise ValidationError({"detail": "contact already exists"})

        if not contact_name:
            attrs["contact_name"] = profile_user.username

        return attrs


class BlockedUserSerializer(ModelSerializer):
    class Meta:
        model = BlockUserModel
        fields = (
            "id",
            "blocked_user",
            "create_at",
            "expired_at",
        )
        extra_kwargs = {
            "blocked_message": {"default": True},
            "blocked_calls": {"default": True},
        }

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        request: Request = self.context.get("request")
        user: UserDataclass = request.user
        blocked_user: BlockUserDataclass = attrs.get("blocked_user")

        if BlockUserModel.objects.filter(user=user, blocked_user=blocked_user).first():
            raise ValidationError("This user is already blocked")

        if user == blocked_user:
            raise ValidationError({"detail": "you can't add yourself"})

        return attrs
