from django.conf import settings
from django.db import models

# ——— RBAC Core ———

class Permission(models.Model):
    """
    A *business* permission, not Django's built-in auth.permission.
    Example codename: "resident.read", "resident.write"
    """
    codename = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.codename

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(
        Permission,
        through="RolePermission",
        related_name="roles",
        blank=True,
    )

    def __str__(self) -> str:
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("role", "permission")

class UserRole(models.Model):
    """
    Direct mapping table so a user can have >1 role.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_roles",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="user_roles",
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "role")

# ——— Policy Management ———

ACCESS_LEVEL_CHOICES = [
    ("no_access", "No Access"),
    ("read_only", "Read Only"),
    ("read_write", "Read & Write"),
    ("full_access", "Full Access"),
]

class Policy(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    applies_to = models.JSONField()  # e.g. ["Healthcare Staff", "Auditors"]
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PolicyRule(models.Model):
    policy = models.ForeignKey(Policy, related_name='rules', on_delete=models.CASCADE)
    resource = models.CharField(max_length=100)
    access_level = models.CharField(max_length=20, choices=ACCESS_LEVEL_CHOICES)

    def __str__(self):
        return f"{self.policy.name} — {self.resource}: {self.access_level}"
