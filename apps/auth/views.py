from django.db.models import QuerySet
from django.utils import timezone
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.dataclass.dataclass import SessionDataclass, UserDataclass
from core.services.session_service import OperationbySession

from .models import CodeUserModel
from .serializers import (
    CodeSerialiser,
    LoginSerializer,
    RefreshSerializer,
)
from rest_framework import status


class LogApi(TokenObtainPairView):
    serializer_class = LoginSerializer


class RefreshApi(TokenRefreshView):
    serializer_class = RefreshSerializer


class LogOutAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs) -> Response:
        session: SessionDataclass = self.request.session
        OperationbySession.logout_session(session)
        return Response(status=status.HTTP_204_NO_CONTENT)


class VerifyCodeAPI(GenericAPIView):
    serializer_class = CodeSerialiser

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code: CodeUserModel = serializer.validated_data["code"]
        user: UserDataclass = code.user

        user.is_verificate = True
        user.save()

        return Response("success", status=status.HTTP_204_NO_CONTENT)
