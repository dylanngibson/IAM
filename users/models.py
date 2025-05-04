from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Leave it empty for now; useful later if you need extra columns like
    'phone_number' or 'mfa_enrolled'.
    """

    # Example extension placeholder:
    # department = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username
