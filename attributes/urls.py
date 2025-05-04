from django.urls import path
from .views import AttributeListCreateView, AttributeDetailView

urlpatterns = [
    path("attributes/", AttributeListCreateView.as_view(), name="attr-list-create"),
    path("attributes/<int:pk>/", AttributeDetailView.as_view(), name="attr-detail"),
]
