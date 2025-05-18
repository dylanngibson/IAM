from django.urls import path
from .views import (
    UserList,
    UserDetail,
    MeView,
    UserCreate,
    UserUpdate,
    UserDelete,
)

urlpatterns = [
    path("", UserList.as_view(), name="user-list"),
    path("me/", MeView.as_view(), name="user-me"),
    path("create/", UserCreate.as_view(), name="user-create"),
    path("<int:pk>/", UserDetail.as_view(), name="user-detail"),
    path("<int:pk>/update/", UserUpdate.as_view(), name="user-update"),
    path("<int:pk>/delete/", UserDelete.as_view(), name="user-delete"),
]
