from django.urls import path
from .views import LogApi, RefreshApi, LogOutAPI, VerifyCodeAPI

urlpatterns = [
    path("login/", LogApi.as_view(), name="token_obtain_pair"),
    path("refresh/", RefreshApi.as_view(), name="token_refresh"),
    path("logout/", LogOutAPI.as_view()),
    path("verify_code/", VerifyCodeAPI.as_view()),
]
