from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.conf import settings
from .models import Alert
from .serializers import AlertSerializer
from .utils import create_alert

class RecentAlertsView(generics.ListAPIView):
    """
    GET /api/alerts/recent/?since=<ISO>&level=WARNING&seen=false
    """
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Alert.objects.all()
        since = self.request.query_params.get("since")
        level = self.request.query_params.get("level")
        seen = self.request.query_params.get("seen")
        if since:
            qs = qs.filter(timestamp__gt=since)
        if level:
            qs = qs.filter(level__iexact=level)
        if seen is not None:
            # expect 'true' or 'false'
            val = seen.lower() == "true"
            qs = qs.filter(seen=val)
        return qs[:100]

class UnseenCountView(APIView):
    """
    GET /api/alerts/unseen-count/
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        count = Alert.objects.filter(seen=False).count()
        return Response({"unseen_count": count})

class AcknowledgeAlertView(APIView):
    """
    POST /api/alerts/<id>/ack/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, alert_id):
        try:
            alert = Alert.objects.get(pk=alert_id)
        except Alert.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        alert.seen = True
        alert.save(update_fields=["seen"])
        return Response({"status": "acknowledged"})

class WebhookCreateAlertView(APIView):
    """
    POST /api/alerts/webhook/
    Body: {"level":"ERROR","message":"...","details":{...}}
    Requires header: X-Alert-Token=<shared_secret>
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.headers.get("X-Alert-Token")
        secret = getattr(settings, "ALERT_WEBHOOK_SECRET", None)
        if not secret or token != secret:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        create_alert(
            level=data.get("level", "INFO"),
            message=data.get("message", "No message"),
            details=data.get("details"),
        )
        return Response({"status": "created"}, status=status.HTTP_201_CREATED)
