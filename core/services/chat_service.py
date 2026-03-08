from apps.chats.models import (
    ChatModel,
    ChatMembersModel,
    ChatTypesModel,
    ChatMembersRoleModel,
)
from core.enum.enum import ChatTypesChoice, RoleMembersChoice
from core.dataclass.dataclass import UserDataclass

from typing import Any


def get_or_create_chat(user_1: UserDataclass, user_2: UserDataclass) -> ChatModel:
    chat = (
        ChatModel.objects.filter(
            chat_type__name=ChatTypesChoice.DIRECT, member__user=user_1
        )
        .filter(member__user=user_2)
        .distinct()
        .first()
    )
    if chat:
        return chat

    chat_type = ChatTypesModel.objects.get(name=ChatTypesChoice.DIRECT.value)
    member_role = ChatMembersRoleModel.objects.get(name="member")

    new_chat = ChatModel.objects.create(owner=user_1, chat_type=chat_type)

    ChatMembersModel.objects.create(chat=new_chat, user=user_1, role=member_role)
    ChatMembersModel.objects.create(chat=new_chat, user=user_2, role=member_role)

    return new_chat


def create_group_channel(
    user: UserDataclass, data: dict[str, Any], chat_type_name: str
) -> ChatModel:
    chat_type = ChatTypesModel.objects.get(name=chat_type_name)
    member_role = ChatMembersRoleModel.objects.get(name="member")

    new_group = ChatModel.objects.create(
        name=data.get("name", "chat"),
        owner=user,
        chat_type=chat_type,
    )
    ChatMembersModel.objects.create(user=user, chat=new_group, role=member_role)
    return new_group


# def chat type permission
# check user in chat
# check role, check owner
# action


# add admin
# permision
