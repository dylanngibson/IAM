import logging
from .models import Alert

logger = logging.getLogger("auth_events")  # same CloudWatch handler

def create_alert(level: str, message: str, *, user=None, details=None) -> Alert:
    alert = Alert.objects.create(
        level=level.upper(),
        message=message,
        user=user,
        details=details,
    )
    logger.warning("security_alert", extra={
        "event": "security_alert",
        "alert_level": alert.level,
        "alert_message": alert.message,
        "alert_id": alert.id,
        "user": getattr(user, "username", None),
    })
    return alert
