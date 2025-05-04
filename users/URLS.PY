from django.urls import path
from .views import UserList, UserDetail, MeView

urlpatterns = [
    path("", UserList.as_view(), name="user-list"),
    path("<int:pk>/", UserDetail.as_view(), name="user-detail"),
    path("me/", MeView.as_view(), name="user-me"),
]
