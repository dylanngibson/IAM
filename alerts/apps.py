from django.apps import AppConfig

class AlertsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "alerts"

    def ready(self):
        from django.contrib.auth.signals import user_login_failed
        from .utils import create_alert
        def _on_fail(sender, credentials, request, **kwargs):
            create_alert(
                level="WARNING",
                message=f"Login failed for {credentials.get('username')!r}",
            )
        user_login_failed.connect(_on_fail, weak=False)
