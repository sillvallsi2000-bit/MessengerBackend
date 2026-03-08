from apps.chats.models import ChatMembersModel
from rest_framework.exceptions import PermissionDenied

from core.dataclass.dataclass import ChatMembersDataclass, UserDataclass


class ChatPermissionManage:
    def __init__(self, user: UserDataclass, chat_id: int):
        self.chat_id = chat_id
        self.user = user
        self.chat_member = self.get_chat_member(user)
        self.able_to_manage_role(user)

    def get_chat_member(self, user):
        chat_member = ChatMembersModel.objects.filter(
            user=user, chat_id=self.chat_id
        ).first()
        if not chat_member:
            raise PermissionDenied({"detail": "You are not a member of this chat"})
        return chat_member

    def check_target_in_chat(self, target_user):
        target = ChatMembersModel.objects.filter(
            chat_id=self.chat_id, user=target_user
        ).first()
        if not target:
            raise PermissionDenied({"detail": "target is not in chat"})
        return target

    def check_owner_or_role(self, member: ChatMembersDataclass):
        owner = member.chat.owner_id == member.user.id
        admin = getattr(member.role, "able_to_manage", False)
        return {"owner": owner, "admin": admin}

    def check_hierarchy(self, target_user: UserDataclass):
        target_member = self.get_target_member(target_user)
        user_permission = self.check_owner_or_role(self.chat_member)
        target_permission = self.check_owner_or_role(target_member)
        if target_permission["owner"]:
            raise PermissionDenied({"detail": "can not change role of owner"})
        if target_permission["admin"] and not user_permission["owner"]:
            raise PermissionDenied({"detail": "can not change role of admin "})
        return target_member

    def able_to_manage_role(self, target):
        target = self.check_target_in_chat(target)
        self.check_hierarchy(target)
        return target


class ChatTypePermission:
    def __init__(self, member):
        self.member = member

    def able_to_do_action(self, action):
        if self.member.chat.owner_id == self.member.user.id:
            return True
        if getattr(self.member.role, action):
            return True
        raise PermissionDenied({"detail": f"You don't have permission: {action}"})

    def able_to_invite_user(self):
        return self.able_to_do_action("able_to_invite")

    def able_to_delete(self):
        return self.able_to_do_action("able_to_delete")

    def able_to_update(self):
        return self.able_to_do_action("able_to_update")

    def able_to_pin(self):
        return self.able_to_do_action("able_to_pin")

    def able_to_edit_chat(self):
        return self.able_to_do_action("able_to_edit_chat")

    def able_to_ban(self):
        return self.able_to_do_action("able_to_ban")
