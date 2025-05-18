import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

logger = logging.getLogger("auth_events")

def _log(event: str, request, user=None, **extra):
    logger.info(
        "auth_event",
        extra={
            "event": event,
            "username": getattr(user, "username", None),
            "remote_addr": request.META.get("REMOTE_ADDR"),
            "path": request.path,
            **extra,
        },
    )

def on_login(sender, request, user, **kwargs):
    _log("login_success", request, user)

def on_logout(sender, request, user, **kwargs):
    _log("logout", request, user)

def on_login_fail(sender, credentials, request, **kwargs):
    _log("login_failed", request, None, username=credentials.get("username"))

user_logged_in.connect(on_login)
user_logged_out.connect(on_logout)
user_login_failed.connect(on_login_fail)
