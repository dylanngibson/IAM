from rest_framework import generics, permissions
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdminRole, IsSameDepartment

class UserList(generics.ListAPIView):
    """
    List all users.
    - Admin role sees everyone.
    - Others limited to same department via ABAC.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated & (IsAdminRole | IsSameDepartment)]

    def get_queryset(self):
        qs = super().get_queryset()
        if IsAdminRole().has_permission(self.request, self):
            return qs
        return [u for u in qs if IsSameDepartment().has_object_permission(self.request, self, u)]

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated & (IsAdminRole | IsSameDepartment)]

class MeView(generics.RetrieveAPIView):
    """
    /users/me/ returns the logged-in user.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserCreate(generics.CreateAPIView):
    """
    Admins only: create new user accounts.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class UserUpdate(generics.UpdateAPIView):
    """
    Admins only: update existing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "pk"

class UserDelete(generics.DestroyAPIView):
    """
    Admins only: delete user accounts.
    """
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "pk"
