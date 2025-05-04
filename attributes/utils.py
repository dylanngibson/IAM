"""
match_attributes(user, resource)  ->  True / False
* user & resource may each have zero‑or‑many Attribute rows.
* For hierarchical values (foo/bar/baz) we treat "foo" or "foo/bar"
  as ancestors, so carers assigned to ward "rosewood/level2"
  can access resident records tagged "rosewood/level2/room14".
"""

from functools import lru_cache

from django.db.models import Prefetch
from .models import Attribute, UserAttribute, ResourceAttribute


@lru_cache(maxsize=2048)
def _attribute_set_for_user(user_id: int) -> set[tuple[str, str]]:
    qs = Attribute.objects.filter(userattribute__user_id=user_id).values_list("key", "value")
    return {tuple(row) for row in qs}


def _explode_path(value: str) -> list[str]:
    """
    "rosewood/level2/room14" -> ["rosewood", "rosewood/level2", "rosewood/level2/room14"]
    """
    parts, paths = value.split("/"), []
    for i in range(1, len(parts) + 1):
        paths.append("/".join(parts[:i]))
    return paths


def match_attributes(user, resource) -> bool:
    if not user or user.is_anonymous:
        return False

    # 1. collect user's attribute tuples
    user_attrs = _attribute_set_for_user(user.id)

    # 2. collect resource attribute tuples
    ra_qs = ResourceAttribute.objects.filter(
        content_type__model=resource._meta.model_name, object_id=resource.pk
    ).select_related("attribute")
    res_attrs: set[tuple[str, str]] = set()
    for ra in ra_qs:
        key, value = ra.attribute.key, ra.attribute.value
        if "/" in value:
            # include ancestors for hierarchy match
            for path in _explode_path(value):
                res_attrs.add((key, path))
        else:
            res_attrs.add((key, value))

    # 3. ABAC logic: ALL resource attributes must be satisfied by user
    return res_attrs.issubset(user_attrs)
