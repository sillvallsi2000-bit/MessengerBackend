from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
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


class UserCreateAPI(CreateAPIView):
    serializer_class = UserSerializer


class GetUserAPI(RetrieveAPIView):
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


class UpdateContactAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = ContactsUserSerializers
    permission_classes: tuple[type[IsAuthenticated]] = (IsAuthenticated,)

    def get_object(self, **kwargs) -> UserContactsModel:
        pk = self.kwargs.get("pk")
        return get_object_or_404(UserContactsModel, contact_user=pk)


class ListCreateBlockUserAPI(ListCreateAPIView):
    serializer_class = BlockedUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[BlockUserModel]:
        user = self.request.user
        return BlockUserModel.objects.filter(user=user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
