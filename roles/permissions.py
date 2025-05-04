from rest_framework.permissions import BasePermission
from .policy import can_access


class RBACPermission(BasePermission):
    """
    Usage:
        class PatientRecordView(APIView):
            permission_classes = [RBACPermission]
            required_permission = "resident.read"
    """

    required_permission: str | None = None

    def has_permission(self, request, view):
        perm = getattr(view, "required_permission", self.required_permission)
        if perm is None:  # developer didn’t set it – deny by default
            return False
        return can_access(request.user, perm)
