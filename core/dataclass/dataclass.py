from django.db import models
from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserBaseDataclass:
    id: int
    email: str
    password: str
    is_active: bool
    is_verificate: bool


@dataclass
class DevicesDataclass:
    id: int
    user: UserBaseDataclass
    device_name: str
    device_model: str
    user_agent: str
    os: str
    is_active: bool
    last_login: datetime


@dataclass
class SessionDataclass:
    id: int
    user: UserBaseDataclass
    device_id: int
    refresh_token: str
    refresh_token_expire: datetime
    ip_address: str
    status: str
    last_activity: datetime


@dataclass
class UserProfileDataclass:
    user: UserBaseDataclass
    username: str
    birthday: int
    bio: str
    avatar: str
    name: str
    surname: str
    phone: str


@dataclass
class ContactUserDataclass:
    user: UserBaseDataclass
    contact_user: UserBaseDataclass
    contact_name: str
    created_at: str
    updated_at: str


@dataclass
class BlockUserDataclass:
    user: UserBaseDataclass
    blocked_user: UserBaseDataclass
    create_at: str
    expired_at: str
    blocked_message: bool
    blocked_calls: bool


@dataclass
class UserDataclass:
    id: int
    email: str
    password: str
    is_active: bool
    is_verificate: bool
    devices: DevicesDataclass
    sessions: SessionDataclass
    profile: UserProfileDataclass


@dataclass
class ChatDataclass:
    id: int
    name: str
    is_active: bool
    owner: bool
    chat_type: bool
    avatar: bool
    created_at: bool
    updated_at: bool
    last_message: bool
    last_activity: bool


@dataclass
class ChatMembersRoleDataclass:
    name: str
    able_to_invite: bool
    able_to_delete: bool
    able_to_message: bool
    able_to_update: bool
    able_to_pin: bool
    able_to_edit_chat: bool
    able_to_ban: bool
    able_to_manage: bool


@dataclass
class ChatMembersDataclass:
    chat: ChatDataclass
    user: UserDataclass
    role: ChatMembersRoleDataclass
    joined_at: datetime
    left_at: datetime
    last_read_at: datetime
    is_muted: bool


@dataclass
class ChatInvitationDataclass:
    chat = ChatDataclass
    inviter = ChatMembersDataclass
    invite_url = str
    status = str
    created_at = datetime
    updated_at = datetime
    message = str
