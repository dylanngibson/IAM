from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role and request.user.role.name == 'Admin'

class IsFromSameDepartment(BasePermission):
    def has_permission(self, request, view):
        # Example ABAC logic
        return request.user.is_authenticated and request.user.department == 'IT'
