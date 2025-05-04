from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Alert
from .serializers import AlertSerializer
from .utils import create_alert


class RecentAlertsView(generics.ListAPIView):
    """
    Poll every N seconds:
      GET /api/alerts/recent/?since=2025-05-04T10:00:00Z
    """
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Alert.objects.all()
        since = self.request.query_params.get("since")
        if since:
            qs = qs.filter(timestamp__gt=since)
        return qs[:100]


class AcknowledgeAlertView(generics.UpdateAPIView):
    """
    POST /api/alerts/<id>/ack/
    Marks alert as seen.
    """
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "alert_id"
    queryset = Alert.objects.all()

    def post(self, request, *args, **kwargs):
        alert = self.get_object()
        alert.seen = True
        alert.save(update_fields=["seen"])
        return Response({"status": "acknowledged"})


# ---- Optional: AWS SNS or webhook ingress ----
from rest_framework.views import APIView

class WebhookCreateAlertView(APIView):
    """
    POST JSON: {"level":"ERROR","message":"GuardDuty finding", "details": {...}}
    """
    permission_classes = [permissions.AllowAny]  # restrict with secret token if needed

    def post(self, request):
        data = request.data
        create_alert(
            level=data.get("level", "INFO"),
            message=data.get("message", "No message"),
            details=data.get("details"),
        )
        return Response({"status": "created"}, status=status.HTTP_201_CREATED)
