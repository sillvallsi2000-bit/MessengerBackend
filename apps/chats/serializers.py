from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer, ValidationError

from apps.user.models import UserModel
from core.services.chat_service import create_group_channel, get_or_create_chat

from .models import (
    ChatMembersModel,
    ChatMembersRoleModel,
    ChatModel,
    ChatTypesModel,
    ChatSettingsModel,
    ChatBannedUserModel,
    ChatInvitationModel,
)
from core.permission.chat_permission import ChatTypePermission, ChatPermissionManage
from core.dataclass.dataclass import (
    ChatMembersDataclass,
    UserDataclass,
    ChatDataclass,
)

from core.enum.enum import ChatTypesChoice
from rest_framework.exceptions import PermissionDenied


class ChatSerializer(ModelSerializer):
    class Meta:
        model = ChatModel
        fields = ("id", "owner", "avatar", "last_message", "last_activity", "chat_type")
        read_only_fields = ("last_message", "last_activity", "owner", "chat_type")


class ChatMembersSerializer(ModelSerializer):
    class Meta:
        model = ChatMembersModel
        fields = (
            "id",
            "chat",
            "user",
            "role",
            "joined_at",
            "left_at",
            "last_read_at",
            "is_muted",
        )
        read_only_fields = ("joined_at", "left_at", "last_read_at", "is_muted")

    def validate(self, attrs):
        user: UserDataclass = self.context["request"].user
        chat_id: int = attrs.get("chat_id")

        if not ChatMembersModel.objects.filter(chat_id=chat_id, user=user).first():
            raise PermissionDenied("You are not a member of this chat")

        return attrs


class ChatMembersRoleSerializer(ModelSerializer):
    class Meta:
        model = ChatMembersRoleModel
        fields = (
            "name",
            "able_to_invite",
            "able_to_delete",
            "able_to_message",
            "able_to_update",
            "able_to_pin",
            "able_to_edit_chat",
            "able_to_ban",
            "able_to_manage",
        )


class ChatTypesSerializer(ModelSerializer):
    class Meta:
        model = ChatTypesModel
        fields = ("__all__",)


class ChatSettingsSerializer(ModelSerializer):
    class Meta:
        model = ChatSettingsModel
        fields = ("chat", "allow_members", "is_private", "theme")


class ChatBannedUserSerializer(ModelSerializer):
    class Meta:
        model = ChatBannedUserModel
        fields = (
            "chat",
            "user",
            "banned_by",
            "banned_at",
            "reason",
            "ban_type",
            "expired_at",
        )


class ChatInvitationSerializer(ModelSerializer):
    class Meta:
        model = ChatInvitationModel
        fields = (
            "chat",
            "inviter",
            "invite_url",
            "status",
            "created_at",
            "updated_at",
            "message",
        )


class ChatDirectSerializer(ChatSerializer):
    member = serializers.PrimaryKeyRelatedField(
        queryset=UserModel.objects.all(), write_only=True
    )

    class Meta(ChatSerializer.Meta):
        fields = ChatSerializer.Meta.fields + ("member",)

    def create(self, validated_data):
        member: ChatMembersDataclass = validated_data.pop("member")
        user: UserDataclass = self.context["request"].user
        chat: ChatDataclass = get_or_create_chat(user_1=user, user_2=member)
        return chat


class ChatGroupSerializer(ChatSerializer):
    class Meta(ChatSerializer.Meta):
        fields = ChatSerializer.Meta.fields + ("name",)
        extra_kwargs = {"name": {"required": True}}

    def create(self, validated_data):
        user: UserModel = self.context["request"].user
        chat: ChatModel = create_group_channel(
            user, data=validated_data, chat_type_name=ChatTypesChoice.GROUP
        )
        return chat


class ChatChannelSerializer(ChatGroupSerializer):
    def create(self, validated_data):
        user = self.context["request"].user
        chat = create_group_channel(
            user=user, data=validated_data, chat_type_name=ChatTypesChoice.CHANNEL
        )
        return chat


class AddMemberSerializer(Serializer):
    target_user = serializers.PrimaryKeyRelatedField(
        queryset=UserModel.objects.all(), write_only=True
    )
    chat_id = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        target_user: UserDataclass = attrs.get("target_user")
        user: UserDataclass = self.context["request"].user
        chat_id: int = attrs.get("chat_id")
        member = ChatMembersModel.objects.filter(chat_id=chat_id, user=user).first()
        if not member:
            raise PermissionDenied({"detail": "you are not a member of this chat"})

        ChatTypePermission(member=member).able_to_invite_user()

        if ChatMembersModel.objects.filter(chat_id=chat_id, user=target_user).first():
            raise ValidationError({"detail": "user already in chat"})

        return attrs

    def create(self, validated_data):
        target_user: UserDataclass = validated_data.pop("target_user")
        chat_id: int = validated_data.pop("chat_id")
        member_role = ChatMembersRoleModel.objects.get(name="member")
        chat_member: ChatMembersDataclass = ChatMembersModel.objects.create(
            chat_id=chat_id, user=target_user, role=member_role
        )
        return chat_member


# class ChangeRoleSerializer(Serializer):
#     target_user = serializers.PrimaryKeyRelatedField(
#         queryset=UserModel.objects.all(), write_only=True
#     )
#     role = serializers.PrimaryKeyRelatedField(
#         queryset=ChatMembersRoleModel.objects.all()
#     )
#     chat_id = serializers.IntegerField()

#     def validate(self, attrs):
#         request_user = self.context["request"].user
#         target = self.instance

#         permission = ChatPermissionManage(user=request_user, chat_id=target.chat_id)

#         permission.able_to_manage_role(target.user)

#         return attrs
