from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auth_app"

    # Import signals on app ready so they register with Django
    def ready(self):
        from . import signals  # noqa