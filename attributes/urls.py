# urls.py
from django.urls import path
from .views import (
    AttributeListCreateView, AttributeDetailView,
    UserAttributeListCreateView, UserAttributeDeleteView,
    ResourceAttributeListCreateView, ResourceAttributeDeleteView,
)

urlpatterns = [
    path("attributes/", AttributeListCreateView.as_view(), name="attr-list-create"),
    path("attributes/<int:pk>/", AttributeDetailView.as_view(), name="attr-detail"),

    path(
        "users/<int:user_id>/attributes/",
        UserAttributeListCreateView.as_view(),
        name="userattr-list-create"
    ),
    path(
        "users/<int:user_id>/attributes/<int:pk>/",
        UserAttributeDeleteView.as_view(),
        name="userattr-delete"
    ),

    path(
        "resources/<str:type>/<int:id>/attributes/",
        ResourceAttributeListCreateView.as_view(),
        name="resattr-list-create"
    ),
    path(
        "resources/<str:type>/<int:id>/attributes/<int:pk>/",
        ResourceAttributeDeleteView.as_view(),
        name="resattr-delete"
    ),
]
