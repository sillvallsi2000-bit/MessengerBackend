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
    ChatInvitationModel,
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
    AddBanMembersSerializers,
    UpdateRoleSerializer,
    ChatSettingsSerializer,
    GroupChatSettinsSerializer,
    ChatInvitationSerializer,
    InviteUrlSerializer,
    ChatSerializer,
)

from apps.user.serializers import UserSerializer
from core.dataclass.dataclass import ChatMembersDataclass
from rest_framework.response import Response
from core.permission.chat_permission import ManageRolePermission
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class ListCreateDirectChatAPI(ListCreateAPIView):
    serializer_class = ChatDirectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ChatModel.objects.filter(member__user=user).distinct()


class DestroyDirectChatAPI(DestroyAPIView):
    serializer_class = ChatDirectSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        chat_id = self.kwargs.get("pk")

        return ChatModel.objects.get(id=chat_id, member__user=user)


class CreateGroupAPI(CreateAPIView):
    serializer_class = ChatGroupSerializer
    permission_classes = [IsAuthenticated]


class CreateChannelAPI(ListCreateAPIView):
    serializer_class = ChatChannelSerializer


class UpdateChatSettingsAPI(UpdateAPIView):
    serializer_class = ChatSettingsSerializer

    def get_object(self):
        chat_id = self.kwargs["chat_id"]
        return get_object_or_404(ChatSettingsModel, chat_id=chat_id)


class UpdateGroupSettingsAPI(UpdateAPIView):
    serializer_class = GroupChatSettinsSerializer

    def get_object(self):
        data = self.request.data
        chat_id = self.kwargs["chat_id"]
        user = self.request.user
        serializer = self.get_serializer(
            data=data, context={"user": user, "chat_id": chat_id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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


class BanMemberAPI(CreateAPIView):
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


# invite url


class InviteMemberAPI(CreateAPIView):
    serializer_class = InviteUrlSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chat_id = self.kwargs["chat_id"]
        member = ChatMembersModel.objects.get(user=self.request.user, chat_id=chat_id)

        serializer.save(inviter=member, chat_id=chat_id)


class JoinToChatAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        invite_url = request.data.get("invite_url")
        if not invite_url:
            return Response(
                {"error": "invite_url is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        invite = get_object_or_404(ChatInvitationModel, invite_url=invite_url)
        chat = invite.chat
        user_member, created = ChatMembersModel.objects.get_or_create(
            user=request.user, chat_id=chat.id
        )

        chat.member.add(user_member)

        return Response(
            {
                "chat_id": chat.id,
                "joined_user": request.user.id,
                "invite_url": invite.invite_url,
            },
            status=status.HTTP_200_OK,
        )


class ChatRetrieveAPI(RetrieveAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        return ChatModel.objects.all()


class ListAllChatsAPI(ListCreateAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        return ChatModel.objects.all()


# chat type all obj,
# add chat members list
# function => obj chat => chattype.direct => chatmembers.username() or  name required
# username required(in User)


# data in outlate
# websocket as outlet
# or redux
# SpecificChatForm (user(me)) => from layout , chat_data => chat.id (vereficate if we are in chat)
# List Message => in SPCform
