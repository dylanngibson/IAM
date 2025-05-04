

from rest_framework.permissions import BasePermission
from roles.policy import has_permission
from attributes.utils import match_attributes


class IsAdminRole(BasePermission):

    required_permission = "admin.panel"

    def has_permission(self, request, view):
        return has_permission(request.user, self.required_permission)


class IsSameDepartment(BasePermission):
 

    def has_object_permission(self, request, view, obj):
        # 'obj' is the target User instance
        return match_attributes(request.user, obj)
