"""
Simple, fast RBAC evaluator with optional in-memory caching.

ABAC rules can be bolted on later by extending `can_access`.
"""

from functools import lru_cache
from typing import Any

from django.contrib.auth import get_user_model
from .models import Permission


@lru_cache(maxsize=4096)
def _permissions_for_user(user_id: int) -> set[str]:
    """
    Returns a *set* of permission codenames for quick O(1) lookups.
    Cached per user id while the process lives.
    """
    qs = Permission.objects.filter(
        roles__user_roles__user_id=user_id
    ).values_list("codename", flat=True)
    return set(qs)


def invalidate_permission_cache(user_id: int) -> None:
    """Call this from signals when roles/permissions change."""
    _permissions_for_user.cache_clear()


def has_permission(user, codename: str) -> bool:
    if not user or user.is_anonymous:
        return False
    return codename in _permissions_for_user(user.id)


def can_access(user, action: str, resource: Any = None) -> bool:
    """
    Generic helper. `action` is a permission codename.
    Ignore `resource` for pure RBAC; keep it for ABAC expansion.
    """
    return has_permission(user, action)
