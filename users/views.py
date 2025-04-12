from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmin, IsFromSameDepartment
from rest_framework.permissions import IsAuthenticated

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsFromSameDepartment]
