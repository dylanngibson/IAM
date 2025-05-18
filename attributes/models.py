# models.py
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Attribute(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ("key", "value")

    def __str__(self):
        return f"{self.key}={self.value}"

class UserAttribute(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attributes"
    )
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "attribute")

class ResourceAttribute(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    resource = GenericForeignKey("content_type", "object_id")
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("content_type", "object_id", "attribute")

    def __str__(self):
        return f"{self.resource} ← {self.attribute}"
