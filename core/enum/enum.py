from django.db import models


class UserSessionStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    EXPIRED = "expired", "Expired"
    BLOCKED = "blocked", "Blocked"
    LOGOUT = "logout", "Logout"


class DeviceType(models.TextChoices):
    PHONE = "phone", "Phone"
    TABLET = "tablet", "Tablet"
    DESKTOP = "desktop", "Desktop"
    WEB = "web", "Web"


class ThemeChoice(models.TextChoices):
    LIGHT = "light", "Light"
    DARK = "dark", "Dark"


class LanguageChoice(models.TextChoices):
    EN = "en", "En"
    UK = "uk", "Uk"


class ChatTypesChoice(models.TextChoices):
    DIRECT = "direct", "Direct"
    GROUP = "group", "Group"
    CHANNEL = "channel", "Channel"


class RoleMembersChoice(models.TextChoices):
    ADMIN = "admin", "Admin"
    MEMBER = "member", "Member"


class ChatBannedUserChoice(models.TextChoices):
    TEMPORARY = "temporary", "Temporary"
    PERMANENT = "permanent", "Permanent"
    MUTE = "mute", "Mute"


class ChatInvitationChoice(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    DECLINED = "declined", "Declined"
    EXPIRED = "expired", "Expired"


class MessageTypeChoices(models.TextChoices):
    TEXT = "TEXT", "Text"
    IMAGE = "IMAGE", "Image"
    VIDEO = "VIDEO", "Video"
