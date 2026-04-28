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

from apps.user.models import ProfileUserModel
from core.enum.enum import ChatTypesChoice
from rest_framework.exceptions import PermissionDenied
from core.services.chat_service import create_role, update_role
from core.services.chat_service import generate_invite_url

from rest_framework.permissions import IsAuthenticated
from apps.user.serializers import UserProfileSerializer
from django.shortcuts import get_object_or_404
from apps.user.serializers import UserSerializer

from apps.messages.serializers import MessagesSerializer
from apps.messages.models import MessagesModel


class ChatMembersSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

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
        fields = "__all__"


class ChatSerializer(ModelSerializer):
    member = ChatMembersSerializer(read_only=True, many=True)
    chat_type = ChatTypesSerializer(read_only=True)
    name = serializers.SerializerMethodField()
    # count = serializers.SerializerMethodField()

    class Meta:
        model = ChatModel
        fields = (
            "id",
            "owner",
            "avatar",
            "last_message",
            "last_activity",
            "chat_type",
            "member",
            "name",
        )
        read_only_fields = ("last_message", "last_activity", "owner", "chat_type")

    def get_name(self, obj):
        request = self.context.get("request")
        if obj.chat_type.name == "group":
            return obj.name

        if obj.chat_type.name == "direct":
            if not request or not request.user:
                return obj.name

            other_member = obj.member.exclude(user=request.user).first()
            if other_member:
                return other_member.user.username

        return obj.name

    # def get_count(self, obj):
    #     user = self.context["request"].user
    #     return (
    #         MessagesModel.objects.filter(chat=obj)
    #         .exclude(sender=user)
    #         .exclude(statuses__user=user, statuses__read_at__isnull=False)
    #         .count()
    #     )


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
        read_only_fields = (
            "chat",
            "inviter",
            "invite_url",
            "status",
            "message",
        )


# chat


class ChatSettingsSerializer(ModelSerializer):
    class Meta:
        model = ChatSettingsModel
        fields = ("chat", "allow_members", "is_private", "theme")
        read_only_fields = ("chat",)


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
    profile = serializers.SerializerMethodField()

    class Meta(ChatSerializer.Meta):
        fields = ChatSerializer.Meta.fields + ("member", "profile")

    def create(self, validated_data):
        member: ChatMembersDataclass = validated_data.pop("member")
        user: UserDataclass = self.context["request"].user
        chat: ChatDataclass = get_or_create_chat(owner=user, target_user=member)
        chat_settings, created = ChatSettingsModel.objects.get_or_create(chat=chat)
        return chat

    def get_profile(self, obj):
        request_user = self.context["request"].user

        target = obj.member.exclude(user=request_user).first()
        profile = ProfileUserModel.objects.filter(user=target.user).first()

        return UserProfileSerializer(profile).data


class ChatGroupSerializer(ChatSerializer):
    name = serializers.CharField(required=True, min_length=1)

    class Meta(ChatSerializer.Meta):
        fields = ChatSerializer.Meta.fields + ("name",)
        extra_kwargs = {"name": {"required": True}}

    def create(self, validated_data):
        user = self.context["request"].user
        chat = create_group_channel(
            user, data=validated_data, name=ChatTypesChoice.GROUP
        )
        chat_settings, created = ChatSettingsModel.objects.get_or_create(chat=chat)
        return chat


class ChatChannelSerializer(ChatGroupSerializer):
    permission_classes = [IsAuthenticated]

    def create(self, validated_data):
        user = self.context["request"].user
        chat = create_group_channel(
            user=user, data=validated_data, name=ChatTypesChoice.CHANNEL
        )
        return chat


class GroupChatSettinsSerializer(ChatSettingsSerializer):
    def validate(self, attrs):
        user = self.context["user"]
        chat_id = self.context["user_id"]
        chat_permission = ManageRolePermission(user=user, chat_id=chat_id)
        chat_permission.able_to_edit_chat()
        return attrs


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


# invite url


class InviteUrlSerializer(ChatInvitationSerializer):
    def create(self, validated_data):
        validated_data["invite_url"] = generate_invite_url()

        return ChatInvitationModel.objects.create(**validated_data)


class SearchAllSerializer(Serializer):
    users = UserSerializer(read_only=True, many=True)
    messeges = MessagesSerializer(read_only=True, many=True)
    group = ChatGroupSerializer(read_only=True, many=True)
