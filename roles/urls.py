from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet,
    PermissionListCreateView,
    PermissionDetailView,
    PolicyCreateView,
)

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')

urlpatterns = [
    # RBAC
    path('permissions/', PermissionListCreateView.as_view(), name='perm-list-create'),
    path('permissions/<int:pk>/', PermissionDetailView.as_view(), name='perm-detail'),
    path('', include(router.urls)),

    # Policy management
    path('policies/', PolicyCreateView.as_view(), name='create-policy'),
]
