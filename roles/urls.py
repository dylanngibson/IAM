from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet,
    PermissionListCreateView, PermissionDetailView,
    PolicyListCreateView, PolicyDetailView,
    UserRoleListCreateView, UserRoleDeleteView,
)

router = DefaultRouter()
router.register(r"roles", RoleViewSet, basename="role")

urlpatterns = [
    # RBAC
    path("permissions/", PermissionListCreateView.as_view(), name="perm-list-create"),
    path("permissions/<int:pk>/", PermissionDetailView.as_view(), name="perm-detail"),
    path("", include(router.urls)),

    # User–Role assignments
    path("user-roles/", UserRoleListCreateView.as_view(), name="userrole-list-create"),
    path("user-roles/<int:pk>/", UserRoleDeleteView.as_view(), name="userrole-delete"),

    # Policy management
    path("policies/", PolicyListCreateView.as_view(), name="policy-list-create"),
    path("policies/<int:pk>/", PolicyDetailView.as_view(), name="policy-detail"),
]
