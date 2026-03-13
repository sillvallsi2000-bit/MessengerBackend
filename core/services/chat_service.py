from apps.chats.models import (
    ChatModel,
    ChatMembersModel,
    ChatTypesModel,
    ChatMembersRoleModel,
)
from core.enum.enum import ChatTypesChoice, RoleMembersChoice
from core.dataclass.dataclass import UserDataclass

from typing import Any


from apps.chats.models import ChatMembersRoleModel, ChatModel


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


def create_group_channel(
    user: UserDataclass,
    data: dict[str, Any],
) -> ChatModel:
    chat_type = ChatTypesModel.objects.get(name=ChatTypesChoice.GROUP)
    new_group = ChatModel.objects.create(
        name=data.get("name", "chat"),
        owner=user,
        chat_type=chat_type,
    )

    ChatMembersModel.objects.create(user=user, chat=new_group)

    return new_group


def change_or_create_role(target_user: UserDataclass, chat_id: int, data):

    member = ChatMembersModel.objects.filter(user=target_user, chat_id=chat_id).first()

    if member.role:
        role = member.role
        for attrs, value in data.items():
            setattr(role, attrs, value)
        role.save()
        role = ChatMembersRoleModel.objects.create(**data)
        member.role = role
        member.save()

    return role
