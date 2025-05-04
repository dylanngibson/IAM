from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from django_otp import devices_for_user

from .models import PendingMFAToken
from .serializers import UsernamePasswordSerializer, MFAVerifySerializer


class LoginView(APIView):
    """
    Step 1 of 2: verify username/password.
    If user has a confirmed OTP device we *require* MFA; otherwise
    we hand out JWTs immediately.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = UsernamePasswordSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.validated_data["user"]

        if devices_for_user(user, confirmed=True).exists():
            pending = PendingMFAToken.objects.create(user=user)
            return Response(
                {
                    "mfa_required": True,
                    "mfa_token": str(pending.id),
                    "expires_in": 300,
                },
                status=status.HTTP_202_ACCEPTED,
            )

        return self._issue_tokens(user)

    @staticmethod
    def _issue_tokens(user):
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )


class MFAVerifyView(APIView):
    """Step 2: verify OTP and hand out JWTs."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = MFAVerifySerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )


class LogoutView(APIView):
    """
    Black-lists the REFRESH token sent by the client.
    Send JSON: {"refresh": "<token>"}
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        from rest_framework_simplejwt.tokens import RefreshToken

        refresh_raw = request.data.get("refresh")
        if not refresh_raw:
            return Response({"detail": "Refresh token missing"}, status=400)

        try:
            token = RefreshToken(refresh_raw)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid refresh token"}, status=400)

        # also wipe the user's outstanding pending-MFA tokens
        request.user.pending_mfa_tokens.all().delete()
        return Response({"message": "Logged out successfully"})
