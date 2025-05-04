from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, PermissionListCreateView, PermissionDetailView

router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')

urlpatterns = [
    path('permissions/', PermissionListCreateView.as_view(), name='perm-list-create'),
    path('permissions/<int:pk>/', PermissionDetailView.as_view(), name='perm-detail'),
    path('', include(router.urls)),  # Must be last to avoid overlap issues
]
