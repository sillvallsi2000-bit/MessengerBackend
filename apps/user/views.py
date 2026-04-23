from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    ListAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError


from .models import (
    BlockUserModel,
    UserContactsModel,
    ProfileUserModel,
    UserSettingsModel,
    UserPrivatyModel,
    UserModel,
)
from .serializers import (
    BlockedUserSerializer,
    ContactsUserSerializers,
    UserPrivatySerializer,
    UserProfileSerializer,
    UserSerializer,
    UserSettingsSerializer,
)
from apps.user.models import ProfileUserModel
from apps.chats.models import ChatModel


class UserCreateAPI(CreateAPIView):
    serializer_class = UserSerializer


class GetUserAPI(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserUpdateAPI(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserProfileAPI(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> ProfileUserModel:
        return self.request.user.profile


class UserSettingsAPI(RetrieveUpdateAPIView):
    serializer_class = UserSettingsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> UserSettingsModel:
        return self.request.user.user_settings


class UserPrivatyAPI(RetrieveUpdateAPIView):
    serializer_class = UserPrivatySerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> UserPrivatyModel:
        return self.request.user.user_privaty


class ListCreateContactUserAPI(ListCreateAPIView):
    serializer_class = ContactsUserSerializers
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return UserContactsModel.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveUpdateContactAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ContactsUserSerializers
    permission_classes: tuple[type[IsAuthenticated]] = (IsAuthenticated,)

    def get_queryset(self):
        return UserContactsModel.objects.filter(user=self.request.user)


class ListCreateBlockUserAPI(ListCreateAPIView):
    serializer_class = BlockedUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[BlockUserModel]:
        user = self.request.user
        return BlockUserModel.objects.filter(user=user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class UnblockUserAPI(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return get_object_or_404(
            BlockUserModel,
            user=self.request.user,
            blocked_user=self.kwargs["blocked_user_id"],
        )


class SearchContactsUserByName(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        user = self.request.user
        target_username = self.kwargs["username"]
        contacts = UserContactsModel.objects.filter(
            user=user, contact_user__profile__username=target_username
        ).first()
        if not contacts:
            raise ValidationError({"detail": "not a contact"})
        return contacts.contact_user.profile


class SearchUserByName(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        target_username = self.kwargs["username"]
        try:
            return UserModel.objects.get(username=target_username)
        except UserModel.DoesNotExist:
            raise ValidationError({"detail": "not a contact"})


class RetrieveUserByIdAPI(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        target_user_id = self.kwargs.get("pk")
        return UserModel.objects.get(id=target_user_id)


class ListUserAPI(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user

        return (
            UserModel.objects.filter(member__chat__member__user=user)
            .exclude(id=user.id)
            .distinct()
        )
