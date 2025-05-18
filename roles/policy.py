"""
Simple, fast RBAC evaluator with optional in-memory caching.

ABAC/policy rules can be bolted on later by extending `can_access`.
"""
from functools import lru_cache
from typing import Any

from django.contrib.auth import get_user_model
from .models import Permission

@lru_cache(maxsize=4096)
def _permissions_for_user(user_id: int) -> set[str]:
    qs = Permission.objects.filter(
        roles__user_roles__user_id=user_id
    ).values_list("codename", flat=True)
    return set(qs)

def invalidate_permission_cache(user_id: int) -> None:
    _permissions_for_user.cache_clear()

def has_permission(user, codename: str) -> bool:
    if not user or user.is_anonymous:
        return False
    return codename in _permissions_for_user(user.id)

def can_access(user, action: str, resource: Any = None) -> bool:
    # Pure RBAC check
    return has_permission(user, action)
