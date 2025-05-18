from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Role, Permission, Policy, UserRole
from .serializers import (
    RoleSerializer,
    PermissionSerializer,
    PolicySerializer,
    UserRoleSerializer,
)

# ——— Custom staff-only permission ———

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

# ——— RBAC Endpoints ———

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsStaff]

    @action(detail=True, methods=['post'])
    def set_permissions(self, request, pk=None):
        role = self.get_object()
        perm_names = request.data.get("permissions", [])
        perms = Permission.objects.filter(name__in=perm_names)
        role.permissions.set(perms)
        return Response({"status": "permissions set"})

    @action(detail=True, methods=["post"])
    def remove_permissions(self, request, pk=None):
        role = self.get_object()
        perm_names = request.data.get("permissions", [])
        perms = Permission.objects.filter(name__in=perm_names)
        role.permissions.remove(*perms)
        return Response({"status": "permissions removed"})

class PermissionListCreateView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsStaff]

class PermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsStaff]

# ——— UserRole Endpoints ———

class UserRoleListCreateView(generics.ListCreateAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsStaff]

class UserRoleDeleteView(generics.DestroyAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsStaff]
    lookup_field = "pk"

# ——— Policy Management Endpoints ———

class PolicyListCreateView(generics.ListCreateAPIView):
    """
    GET /roles/policies/ → list all policies
    POST /roles/policies/ → create a new policy + its rules
    """
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [IsStaff]

class PolicyDetailView(generics.RetrieveDestroyAPIView):
    """
    GET /roles/policies/<id>/ → retrieve a policy
    DELETE /roles/policies/<id>/ → delete a policy
    """
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    permission_classes = [IsStaff]
