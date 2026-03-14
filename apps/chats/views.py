from rest_framework.generics import (
    ListCreateAPIView,
    CreateAPIView,
    GenericAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import (
    ChatModel,
    ChatMembersModel,
    ChatMembersRoleModel,
    UserModel,
    ChatSettingsModel,
)
from .serializers import (
    ChatDirectSerializer,
    ChatGroupSerializer,
    ChatChannelSerializer,
    AddRoleSerializer,
    AddMembersToChatSerializer,
    ChatMembersSerializer,
    ChatMembersRoleSerializer,
    FullMemberSerializer,
    ChatBannedUserSerializer,
    AddBanMembersSerializers,
    UpdateRoleSerializer,
    ChatSettingsSerializer,
)

from apps.user.serializers import UserSerializer
from core.dataclass.dataclass import ChatMembersDataclass
from rest_framework.response import Response
from core.permission.chat_permission import ManageRolePermission
from rest_framework.exceptions import ValidationError


class ListCreateDirectChatAPI(ListCreateAPIView):
    serializer_class = ChatDirectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatModel.objects.filter(member__user=user).distinct()


class CreateGroupAPI(CreateAPIView):
    serializer_class = ChatGroupSerializer
    permission_classes = [IsAuthenticated]


class CreateChannelAPI(ListCreateAPIView):
    serializer_class = ChatChannelSerializer


class UpdateChatSettingsAPI(UpdateAPIView):
    serializer_class = ChatSettingsSerializer


# ------
class CreateMembersAPI(GenericAPIView):
    serializer_class = AddMembersToChatSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        user = self.request.user
        chat_id = self.kwargs.get("chat_id")
        serializer = self.get_serializer(
            data=data, context={"user": user, "chat_id": chat_id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateMembersAPI(GenericAPIView):
    serializer_class = UpdateRoleSerializer

    def post(self, *args, **kwargs):
        data = self.request.data
        user = self.request.user
        chat_id = self.kwargs.get("chat_id")
        serializer = self.get_serializer(
            data=data, context={"user": user, "chat_id": chat_id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DestroyMemberAPI(GenericAPIView):
    serializer_class = ChatMembersSerializer

    def delete(self, *args, **kwargs):
        user = self.request.user
        chat_id = kwargs.get("chat_id")
        target_id = kwargs.get("target_id")
        member = ChatMembersModel.objects.filter(
            chat_id=chat_id, user_id=target_id
        ).first()

        permission = ManageRolePermission(user=user, chat_id=chat_id)
        permission.able_to_delete()
        member.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class GetMeInfoAPI(RetrieveAPIView):
    serializer_class = FullMemberSerializer

    def get_object(self):
        chat_id = self.kwargs["chat_id"]
        user = self.request.user
        return ChatMembersModel.objects.get(chat_id=chat_id, user=user)


# ------


class AddRoleChatAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddRoleSerializer

    def post(self, *args, **kwargs):
        chat_id = self.kwargs.get("pk")
        user = self.request.user
        data = self.request.data
        serializer = self.get_serializer(
            data=data, context={"user": user, "chat_id": chat_id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DestroyMemberRoleAPI(GenericAPIView):
    serializer_class = ChatMembersRoleSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, *args, **kwargs):
        chat_id = self.kwargs["chat_id"]
        target_id = self.kwargs["target_id"]
        user = self.request.user
        member: ChatMembersDataclass = ChatMembersModel.objects.filter(
            chat_id=chat_id, user_id=target_id
        ).first()
        role = member.role
        if not member.role:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        permission = ManageRolePermission(user=user, chat_id=chat_id)
        permission.able_to_delete()
        role.delete()
        member.role = None
        member.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BanUserAPI(CreateAPIView):
    serializer_class = AddBanMembersSerializers
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        chat_id = self.kwargs["chat_id"]
        data = self.request.data
        serializer = self.get_serializer(
            data=data, context={"user": user, "chat_id": chat_id}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
