from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django_otp import devices_for_user

from .models import PendingMFAToken

class UsernamePasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        user = authenticate(username=attrs["username"], password=attrs["password"])
        if not user:
            raise AuthenticationFailed("Invalid credentials")
        attrs["user"] = user
        return attrs

class MFAVerifySerializer(serializers.Serializer):
    mfa_token = serializers.UUIDField()
    otp = serializers.CharField()

    def validate(self, attrs):
        try:
            pending = PendingMFAToken.objects.select_related("user").get(id=attrs["mfa_token"])
        except PendingMFAToken.DoesNotExist:
            raise AuthenticationFailed("Invalid or expired MFA token")

        if pending.is_expired:
            pending.delete()
            raise AuthenticationFailed("MFA token expired")

        user = pending.user
        for device in devices_for_user(user, confirmed=True):
            if device.verify_token(attrs["otp"]):
                attrs["user"] = user
                pending.delete()
                return attrs

        raise AuthenticationFailed("Incorrect OTP")
