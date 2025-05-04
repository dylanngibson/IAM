from django.urls import path

from .views import LoginView, MFAVerifyView, LogoutView

urlpatterns = [
    path("login/", LoginView.as_view(), name="api-login"),
    path("mfa/verify/", MFAVerifyView.as_view(), name="api-mfa-verify"),
    path("logout/", LogoutView.as_view(), name="api-logout"),
]
