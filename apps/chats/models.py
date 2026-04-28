from django.db import models
from apps.user.models import UserModel
from core.enum.enum import (
    ChatTypesChoice,
    ChatBannedUserChoice,
    ChatInvitationChoice,
)


class ChatTypesModel(models.Model):
    class Meta:
        db_table = "chat_types"

    name = models.CharField(max_length=20, choices=ChatTypesChoice.choices)
    description = models.CharField(max_length=100, null=True, blank=True)
    is_edit_message = models.BooleanField(default=True)
    is_delete_message = models.BooleanField(default=True)
    is_add_members = models.BooleanField(default=True)
    is_add_message = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ChatModel(models.Model):
    class Meta:
        db_table = "chats"

    name = models.CharField(
        max_length=50,
    )
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="chat")
    chat_type = models.ForeignKey(ChatTypesModel, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_message = models.ForeignKey(
        "messages.MessagesModel",
        on_delete=models.CASCADE,
        related_name="last_message_for_chats",
        null=True,
        blank=True,
    )
    last_activity = models.DateTimeField(blank=True, null=True)


class ChatMembersRoleModel(models.Model):
    class Meta:
        db_table = "members_role"

    name = models.CharField(max_length=50)
    able_to_invite = models.BooleanField(default=False)
    able_to_delete = models.BooleanField(default=False)
    able_to_message = models.BooleanField(default=True)
    able_to_update = models.BooleanField(default=False)
    able_to_pin = models.BooleanField(default=False)
    able_to_edit_chat = models.BooleanField(default=False)
    able_to_ban = models.BooleanField(default=False)
    able_to_manage = models.BooleanField(default=False)


class ChatMembersModel(models.Model):
    class Meta:
        db_table = "members"

    chat = models.ForeignKey(ChatModel, on_delete=models.CASCADE, related_name="member")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="member")
    role = models.OneToOneField(
        ChatMembersRoleModel,
        on_delete=models.CASCADE,
        related_name="member",
        null=True,
        blank=True,
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(blank=True, null=True)
    last_read_at = models.DateTimeField(blank=True, null=True)
    is_muted = models.BooleanField(default=False)


class ChatSettingsModel(models.Model):
    class Meta:
        db_table = "chat_settings"

    chat = models.OneToOneField(
        ChatModel, on_delete=models.CASCADE, related_name="settings"
    )
    allow_members = models.BooleanField(default=True)
    is_private = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    theme = models.CharField(max_length=250)


class ChatBannedUserModel(models.Model):
    class Meta:
        db_table = "chat_banned"

    chat = models.ForeignKey(ChatModel, on_delete=models.CASCADE, related_name="banned")
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="banned_as_user"
    )
    banned_by = models.ForeignKey(
        ChatMembersModel, on_delete=models.CASCADE, related_name="banned_by_user"
    )
    banned_at = models.DateTimeField(auto_now=True)
    reason = models.CharField(max_length=100)
    ban_type = models.CharField(max_length=40, choices=ChatBannedUserChoice.choices)
    expired_at = models.DateTimeField(auto_now_add=True)


class ChatInvitationModel(models.Model):
    class Meta:
        db_table = "chat_invitation"

    chat = models.ForeignKey(
        ChatModel, on_delete=models.CASCADE, related_name="invitation"
    )
    inviter = models.ForeignKey(
        ChatMembersModel, on_delete=models.CASCADE, related_name="sent_invitation"
    )
    invite_url = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=40, choices=ChatInvitationChoice.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=100)


# update_member
# chat_settings
# edit_chat
# chat_type(permission)
# invite link
