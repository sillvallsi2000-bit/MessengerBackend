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
from core.permission.chat_permission import ChatPermissionManage, ManageRolePermission
from core.dataclass.dataclass import (
    ChatMembersDataclass,
    UserDataclass,
    ChatDataclass,
)

from core.enum.enum import ChatTypesChoice
from rest_framework.exceptions import PermissionDenied
from core.services.chat_service import create_role, update_role


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
            "id",
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


# chat


class ChatSettingsSerializer(ModelSerializer):
    class Meta:
        model = ChatSettingsModel
        fields = ("chat", "allow_members", "is_private", "theme")


class FullMemberSerializer(ModelSerializer):
    chat = ChatSerializer()
    role = ChatMembersRoleSerializer()

    class Meta:
        model = ChatMembersModel
        fields = "__all__"


class ChatDirectSerializer(ChatSerializer):
    member = serializers.PrimaryKeyRelatedField(
        queryset=UserModel.objects.all(), write_only=True
    )

    class Meta(ChatSerializer.Meta):
        fields = ChatSerializer.Meta.fields + ("member",)

    def create(self, validated_data):
        member: ChatMembersDataclass = validated_data.pop("member")
        user: UserDataclass = self.context["request"].user
        chat: ChatDataclass = get_or_create_chat(owner=user, target_user=member)
        chat_settings, created = ChatSettingsModel.objects.get_or_create(chat=chat)
        return chat


class ChatGroupSerializer(ChatSerializer):
    class Meta(ChatSerializer.Meta):
        fields = ChatSerializer.Meta.fields + ("name",)
        extra_kwargs = {"name": {"required": True}}

    def create(self, validated_data):
        user = self.context["request"].user
        chat = create_group_channel(user, data=validated_data)
        return chat


class ChatChannelSerializer(ChatGroupSerializer):
    def create(self, validated_data):
        user = self.context["request"].user
        chat = create_group_channel(
            user=user, data=validated_data, chat_type_name=ChatTypesChoice.CHANNEL
        )
        return chat


class ChatUpdateSettingsSerializer(ChatSettingsSerializer):
    def validate(self, attrs):
        user = self.context["user"]
        chat_id = self.context["chat_id"]
        chat_permission = ManageRolePermission(user=user, chat_id=chat_id)
        chat_permission.able_to_edit_chat()
        return attrs

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


# roles


class AddRoleSerializer(ChatMembersRoleSerializer):
    target_user = serializers.PrimaryKeyRelatedField(
        queryset=UserModel.objects.all(), write_only=True
    )

    class Meta(ChatMembersRoleSerializer.Meta):
        fields = ChatMembersRoleSerializer.Meta.fields + ("target_user",)

    def validate(self, attrs):
        target_user = attrs.get("target_user")
        chat_id = self.context.get("chat_id")
        user = self.context["user"]
        chat_permission = ChatPermissionManage(
            user=user, target_user=target_user, chat_id=chat_id
        )
        chat_permission.able_to_manage_role()
        return attrs

    def create(self, validated_data):
        target_user = validated_data.pop("target_user")
        chat_id = self.context.get("chat_id")
        member_role = create_role(
            target_user=target_user, chat_id=chat_id, data=validated_data
        )

        return member_role


class UpdateRoleSerializer(ChatMembersSerializer):
    target_user = serializers.PrimaryKeyRelatedField(
        queryset=UserModel.objects.all(), write_only=True
    )

    class Meta(ChatMembersRoleSerializer.Meta):
        fields = ChatMembersRoleSerializer.Meta.fields + ("target_user",)

    def validate(self, attrs):
        target_user = attrs.get("target_user")
        chat_id = self.context.get("chat_id")
        user = self.context["user"]
        chat_permission = ChatPermissionManage(
            user=user, target_user=target_user, chat_id=chat_id
        )
        chat_permission.able_to_manage_role()
        return attrs

    def create(self, validated_data):
        target_user = validated_data.pop("target_user")
        chat_id = self.context.get("chat_id")
        member_role = update_role(
            target_user=target_user, chat_id=chat_id, data=validated_data
        )
        return member_role


# members


class AddMembersToChatSerializer(Serializer):
    target_user = serializers.PrimaryKeyRelatedField(
        queryset=UserModel.objects.all(), write_only=True
    )

    def validate(self, attrs):
        user = self.context["user"]
        chat_id = self.context.get("chat_id")

        chat_permission = ManageRolePermission(user=user, chat_id=chat_id)
        chat_permission.able_to_add_chat()

        return attrs

    def create(self, validated_data):
        target_user = validated_data.pop("target_user")
        chat_id = self.context.get("chat_id")
        member = ChatMembersModel.objects.create(chat_id=chat_id, user=target_user)
        return member


class AddBanMembersSerializers(Serializer):
    target_user = serializers.PrimaryKeyRelatedField(
        queryset=UserModel.objects.all(), write_only=True
    )

    def validate(self, attrs):
        user = self.context["user"]
        chat_id = self.context["chat_id"]
        chat_permission = ManageRolePermission(user=user, chat_id=chat_id)
        chat_permission.able_to_ban()
        return attrs

    def create(self, validated_data):
        target_user = validated_data.pop("target_user")
        user = self.context["user"]
        chat_id = self.context["chat_id"]
        ban_user = ChatBannedUserModel.objects.create(
            chat_id=chat_id, banned_by=user, user=target_user
        )
        return ban_user
