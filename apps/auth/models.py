from datetime import timedelta

from django.db import models
from django.utils import timezone

from apps.user.models import UserModel
from core.enum.enum import DeviceType, UserSessionStatus


class UserDeviceModel(models.Model):
    class Meta:
        db_table = "user_device"

    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="devices"
    )
    device_name = models.CharField(
        max_length=100,
    )
    device_model = models.CharField(
        max_length=100,
    )
    user_agent = models.CharField(
        max_length=256,
    )
    os = models.CharField(
        max_length=128,
    )
    is_active = models.BooleanField(default=True)
    ip_address = models.CharField(max_length=20, null=True, blank=True)
    device_type = models.CharField(max_length=25, choices=DeviceType.choices)
    last_login = models.DateTimeField(null=True, blank=True)


class UserSessionModel(models.Model):
    class Meta:
        db_table = "user_session"

    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="sessions"
    )
    device = models.ForeignKey(
        UserDeviceModel, on_delete=models.CASCADE, related_name="sessions"
    )
    refresh_token = models.TextField(unique=True)
    refresh_token_expire = models.DateTimeField()
    status = models.CharField(max_length=20, choices=UserSessionStatus.choices)
    last_activity = models.DateTimeField(default=timezone.now)


class CodeUserModel(models.Model):
    class Meta:
        db_table = "user_code"

    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="user_code"
    )
    code = models.CharField(max_length=6)
    verificated_at = models.DateTimeField(null=True, blank=True)
    expired_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expired_at:
            self.expired_at = timezone.now() + timedelta(minutes=15)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expired_at
