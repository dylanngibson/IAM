from django.urls import path
from .views import (
    RecentAlertsView,
    UnseenCountView,
    AcknowledgeAlertView,
    WebhookCreateAlertView,
)

urlpatterns = [
    path("recent/", RecentAlertsView.as_view(), name="alerts-recent"),
    path("unseen-count/", UnseenCountView.as_view(), name="alerts-unseen-count"),
    path("<int:alert_id>/ack/", AcknowledgeAlertView.as_view(), name="alert-ack"),
    path("webhook/", WebhookCreateAlertView.as_view(), name="alert-webhook"),
]
