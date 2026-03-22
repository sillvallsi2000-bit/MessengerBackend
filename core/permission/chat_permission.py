from apps.chats.models import ChatMembersModel, UserModel
from rest_framework.exceptions import PermissionDenied

from core.dataclass.dataclass import ChatMembersDataclass, UserDataclass


class ChatPermissionManage:
    def __init__(self, user: UserDataclass, target_user: UserDataclass, chat_id: int):
        self.chat_id = chat_id
        self.user = user
        self.chat_member = self.get_chat_member(user)
        self.target_user = self.check_target_in_chat(target_user)
        self.get_check_correct_yourself()

    def get_check_correct_yourself(self):
        if self.target_user.user == self.user:
            raise PermissionDenied({"detail": "You are not change yourself permission"})

    def get_chat_member(self, user):
        chat_member = ChatMembersModel.objects.filter(
            user=user, chat_id=self.chat_id
        ).first()
        if not chat_member:
            raise PermissionDenied({"detail": "You are not a member of this chat"})
        return chat_member

    def check_target_in_chat(self, target_user: UserDataclass):
        target = ChatMembersModel.objects.filter(
            user=target_user, chat_id=self.chat_id
        ).first()
        if not target:
            raise PermissionDenied({"detail": "User is not in chat"})
        return target

    def check_owner_or_role(self, member: ChatMembersDataclass):
        owner = member.chat.owner_id == member.user.id
        admin = bool(member.role)
        return {"owner": owner, "admin": admin}

    def check_hierarchy(self):
        user_permission = self.check_owner_or_role(self.chat_member)
        target_permission = self.check_owner_or_role(self.target_user)
        if target_permission["owner"]:
            raise PermissionDenied({"detail": "can not change role of owner"})

        if target_permission["admin"] and not user_permission["owner"]:
            raise PermissionDenied({"detail": "can not change role of admin"})
        return self.target_user

    def able_to_manage_role(self):
        self.check_hierarchy()
        if not self.chat_member.role.able_to_manage:
            raise PermissionDenied({"detail": "You can't assign role"})


class ManageRolePermission:
    def __init__(self, user, chat_id):
        self.chat_id = chat_id
        self.user = user
        self.chat_member = ChatMembersModel.objects.filter(
            user=user, chat_id=chat_id
        ).first()
        if not self.chat_member:
            raise PermissionDenied({"detail": "You are not a member of this chat"})

    def able_to_add_chat(self):
        if not self.chat_member.role:
            raise PermissionDenied({"detail": "Your role is not set in this chat"})
        if not self.chat_member.role.able_to_invite:
            raise PermissionDenied({"detail": "you do not have a permission"})

    def able_to_delete(self):
        if not self.chat_member.role.able_to_delete:
            raise PermissionDenied({"detail": "you do not have a permission"})

    def able_to_update(self):
        if not self.chat_member.role.able_to_update:
            raise PermissionDenied({"detail": "you do not have a permission"})

    def able_to_ban(self):
        if not self.chat_member.role.able_to_ban:
            raise PermissionDenied({"detail": "you do not have a permission"})

    def able_to_pin(self):
        if not self.chat_member.role.able_to_pin:
            raise PermissionDenied({"detail": "you do not have a permission"})

    def able_to_edit_chat(self):
        if not self.chat_member.role.able_to_edit_chat:
            raise PermissionDenied({"detail": "you do not have a permission"})
