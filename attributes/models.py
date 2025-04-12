from django.db import models
from users.models import User

class UserAttribute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=50)  # e.g., 'ward', 'region'
    value = models.CharField(max_length=100)  # e.g., 'north-wing', 'vic'

    def __str__(self):
        return f"{self.user.username}: {self.key} = {self.value}"
