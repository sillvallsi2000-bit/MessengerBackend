from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import UserManager
from core.enum.enum import ThemeChoice, LanguageChoice


class UserModel(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = "auth_user"

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    username = models.CharField(
        max_length=30,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_verificate = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()


class ProfileUserModel(models.Model):
    class Meta:
        db_table = "profile_user"

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="profile",
    )
    birthday = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=250, null=True, blank=True)
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)


class UserSettingsModel(models.Model):
    class Meta:
        db_table = "user_settings"

    user = models.OneToOneField(
        UserModel, on_delete=models.CASCADE, related_name="user_settings"
    )
    theme = models.CharField(
        max_length=20, choices=ThemeChoice.choices, default=ThemeChoice.DARK
    )
    language = models.CharField(
        max_length=20, choices=LanguageChoice.choices, default=LanguageChoice.EN
    )

    notification_enable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserPrivatyModel(models.Model):
    class Meta:
        db_table = "user_privaty"

    user = models.OneToOneField(
        UserModel, on_delete=models.CASCADE, related_name="user_privaty"
    )
    profile_photo_visible = models.BooleanField(default=True)
    allow_message = models.BooleanField(default=True)
    allow_calls = models.BooleanField(default=True)
    forward_message = models.BooleanField(default=True)
    show_phone_number = models.BooleanField(default=True)
    profile_visible = models.BooleanField(default=True)


class UserContactsModel(models.Model):
    class Meta:
        db_table = "contacts_user"

    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="contacts"
    )
    contact_user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="aded_contact"
    )
    contact_name = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BlockUserModel(models.Model):
    class Meta:
        db_table = "block_user"

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="blocks")
    blocked_user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="blocked_by"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateField(null=True, blank=True)


class StatusUserModel(models.Model):
    class Meta:
        db_table = "status_user"

    user = models.OneToOneField(
        UserModel, on_delete=models.CASCADE, related_name="status"
    )
    last_seen_at = models.DateTimeField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    status = models.CharField(max_length=50)
