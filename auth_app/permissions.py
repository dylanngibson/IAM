from rest_framework.permissions import BasePermission
from .policy import PolicyEngine


class IAMPermission(BasePermission):
    """DRF permission class delegating to our policy engine."""

    def has_permission(self, request, view):
        action = view.action if hasattr(view, "action") else request.method
        resource = getattr(view, "resource_name", view.__class__.__name__)
        decision = PolicyEngine.can_access(request.user, action, resource)
        # log decision
        PolicyEngine.log_decision(request.user, action, resource, decision, request)
        return decision