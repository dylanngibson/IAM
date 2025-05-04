from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Role, Permission
from .serializers import RoleSerializer, PermissionSerializer

# Custom permission: only staff can access
class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

# Role ViewSet with custom actions
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsStaff]

    @action(detail=True, methods=['post'])
    def set_permissions(self, request, pk=None):
        role = self.get_object()
        perm_names = request.data.get('permissions', [])
        try:
            perms = Permission.objects.filter(name__in=perm_names)
            role.permissions.set(perms)
            return Response({'status': 'permissions set'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_permissions(self, request, pk=None):
        role = self.get_object()
        perm_names = request.data.get('permissions', [])
        try:
            perms = Permission.objects.filter(name__in=perm_names)
            role.permissions.remove(*perms)
            return Response({'status': 'permissions removed'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Separate views for permission list/create
from rest_framework import generics

class PermissionListCreateView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsStaff]

class PermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsStaff]
