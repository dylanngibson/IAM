# views.py
from rest_framework import generics, permissions
from django.contrib.contenttypes.models import ContentType
from .models import Attribute, UserAttribute, ResourceAttribute
from .serializers import (
    AttributeSerializer,
    UserAttributeSerializer,
    ResourceAttributeSerializer,
)

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

class AttributeListCreateView(generics.ListCreateAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [IsStaff]

class AttributeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [IsStaff]

class UserAttributeListCreateView(generics.ListCreateAPIView):
    serializer_class = UserAttributeSerializer
    permission_classes = [IsStaff]

    def get_queryset(self):
        return UserAttribute.objects.filter(user_id=self.kwargs["user_id"])

    def perform_create(self, serializer):
        serializer.save(user_id=self.kwargs["user_id"])

class UserAttributeDeleteView(generics.DestroyAPIView):
    queryset = UserAttribute.objects.all()
    serializer_class = UserAttributeSerializer
    permission_classes = [IsStaff]
    lookup_field = "pk"

class ResourceAttributeListCreateView(generics.ListCreateAPIView):
    serializer_class = ResourceAttributeSerializer
    permission_classes = [IsStaff]

    def get_queryset(self):
        ct = ContentType.objects.get(model=self.kwargs["type"])
        return ResourceAttribute.objects.filter(
            content_type=ct, object_id=self.kwargs["id"]
        )

    def perform_create(self, serializer):
        ct = ContentType.objects.get(model=self.kwargs["type"])
        serializer.save(
            content_type=ct,
            object_id=self.kwargs["id"]
        )

class ResourceAttributeDeleteView(generics.DestroyAPIView):
    queryset = ResourceAttribute.objects.all()
    serializer_class = ResourceAttributeSerializer
    permission_classes = [IsStaff]
    lookup_field = "pk"
