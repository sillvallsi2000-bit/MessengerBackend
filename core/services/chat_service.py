from apps.chats.models import (
    ChatModel,
    ChatMembersModel,
    ChatTypesModel,
    ChatMembersRoleModel,
)
from core.enum.enum import ChatTypesChoice, RoleMembersChoice
from core.dataclass.dataclass import UserDataclass

from typing import Any

import secrets

from apps.chats.models import ChatMembersRoleModel, ChatModel
from django.db.transaction import atomic


@atomic
def get_or_create_chat(owner: UserDataclass, target_user: UserDataclass) -> ChatModel:
    chat = (
        ChatModel.objects.filter(
            chat_type__name=ChatTypesChoice.DIRECT.value, member__user=owner
        )
        .filter(member__user=target_user)
        .distinct()
        .first()
    )

    if chat:
        return chat

    chat_type = ChatTypesModel.objects.get(name=ChatTypesChoice.DIRECT.value)
    new_chat = ChatModel.objects.create(owner=owner, chat_type=chat_type)
    ChatMembersModel.objects.create(chat=new_chat, user=owner)
    ChatMembersModel.objects.create(chat=new_chat, user=target_user)
    return new_chat


def create_group_channel(user: UserDataclass, data: dict[str, Any], name) -> ChatModel:
    chat_type = ChatTypesModel.objects.get(name=name)
    group_name = data.get("name")
    if not group_name or not group_name.strip():
        raise ValueError("empty name")

    chat_type = ChatTypesModel.objects.get(name=name)

    new_group = ChatModel.objects.create(
        name=group_name.strip(),
        owner=user,
        chat_type=chat_type,
    )

    member = ChatMembersModel.objects.create(user=user, chat=new_group)

    owner_role = {
        "name": "owner",
        "able_to_invite": True,
        "able_to_delete": True,
        "able_to_update": True,
        "able_to_ban": True,
        "able_to_pin": True,
        "able_to_edit_chat": True,
        "able_to_manage": True,
    }
    create_role(target_user=user, chat_id=new_group.id, data=owner_role)

    return new_group


def create_role(target_user: UserDataclass, chat_id: int, data):
    member = ChatMembersModel.objects.filter(user=target_user, chat_id=chat_id).first()

    if member.role:
        return member.role
    role = ChatMembersRoleModel.objects.create(**data)
    member.role = role
    member.save()

    return role


def update_role(target_user: UserDataclass, chat_id: int, data):
    member = ChatMembersModel.objects.filter(user=target_user, chat_id=chat_id).first()
    if not member or not member.role:
        return None

    role = member.role
    for attr, value in data.items():
        setattr(role, attr, value)
    role.save()
    return role


def generate_invite_url():
    return secrets.token_urlsafe(16)
