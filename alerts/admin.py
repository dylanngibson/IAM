from django.contrib import admin
from .models import Alert

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("id", "timestamp", "level", "message", "user", "seen")
    list_filter = ("level", "seen", "timestamp")
    search_fields = ("message", "user__username")
