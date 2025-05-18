from django.urls import path
from .views import LoginView, MFAVerifyView, LogoutView, SetupMFAView

urlpatterns = [
    path("login/", LoginView.as_view(), name="api-login"),
    path("mfa/verify/", MFAVerifyView.as_view(), name="api-mfa-verify"),
    path("mfa/setup/", SetupMFAView.as_view(), name="api-mfa-setup"),
    path("logout/", LogoutView.as_view(), name="api-logout"),
]
