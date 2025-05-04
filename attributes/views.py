from rest_framework import generics, permissions
from .models import Attribute
from .serializers import AttributeSerializer


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class AttributeListCreateView(generics.ListCreateAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [IsStaff]


class AttributeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [IsStaff]
