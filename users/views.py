from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdminRole, IsSameDepartment


class UserList(generics.ListAPIView):
    """
    List all users.
    - Admin role can see everyone.
    - Otherwise limited to same department via ABAC.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated & (IsAdminRole | IsSameDepartment)]

    def get_queryset(self):
        qs = super().get_queryset()
        # If admin → full queryset
        if IsAdminRole().has_permission(self.request, self):
            return qs
        # else ABAC filter: show only users the requester can access
        return [u for u in qs if IsSameDepartment().has_object_permission(self.request, self, u)]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated & (IsAdminRole | IsSameDepartment)]


class MeView(generics.RetrieveAPIView):
    """
    Handy `/users/me/` endpoint for the logged‑in user.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
