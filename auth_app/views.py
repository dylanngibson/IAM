# auth_app/views.py

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice

from .models import PendingMFAToken
from .serializers import UsernamePasswordSerializer, MFAVerifySerializer


class LoginView(APIView):
    """
    Step 1 of 2: verify username/password.
    If user has a confirmed OTP device, require MFA; otherwise issue JWTs.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        ser = UsernamePasswordSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.validated_data["user"]

        # devices_for_user returns a generator, so convert to list first
        confirmed_devices = [
            d for d in devices_for_user(user, confirmed=True)
        ]
        if confirmed_devices:
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
    Blacklists the REFRESH token sent by the client.
    Send JSON: {"refresh": "<token>"}
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_raw = request.data.get("refresh")
        if not refresh_raw:
            return Response({"detail": "Refresh token missing"}, status=400)
        try:
            token = RefreshToken(refresh_raw)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid refresh token"}, status=400)

        # Also clear any outstanding pending MFA tokens
        request.user.pending_mfa_tokens.all().delete()
        return Response({"message": "Logged out successfully"})


class SetupMFAView(APIView):
    """
    GET  /auth/mfa/setup/   → generate TOTP secret & return provisioning URL
    POST /auth/mfa/setup/   → verify OTP and mark device confirmed
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # remove any old unconfirmed devices
        TOTPDevice.objects.filter(user=request.user, confirmed=False).delete()
        # create a new unconfirmed device
        device = TOTPDevice.objects.create(
            user=request.user, name="default", confirmed=False
        )
        return Response({"provisioning_uri": device.config_url})

    def post(self, request):
        otp = request.data.get("otp")
        try:
            device = (
                TOTPDevice.objects
                .filter(user=request.user, confirmed=False)
                .latest("pk")
            )
        except TOTPDevice.DoesNotExist:
            return Response({"detail": "No pending MFA device"}, status=400)

        if device.verify_token(otp):
            device.confirmed = True
            device.save(update_fields=["confirmed"])
            return Response({"message": "MFA setup complete"})
        return Response({"detail": "Invalid OTP"}, status=400)
