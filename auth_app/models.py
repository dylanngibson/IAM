import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class PendingMFAToken(models.Model):
    """
    One-time token issued after a successful password check
    but *before* the user supplies their TOTP code.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pending_mfa_tokens"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_expired(self) -> bool:
        return self.created_at + timedelta(minutes=5) < timezone.now()

    def __str__(self) -> str:
        return f"{self.user} | {self.created_at:%Y-%m-%d %H:%M:%S}"
