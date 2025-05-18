from django.contrib import admin
from .models import PendingMFAToken

@admin.register(PendingMFAToken)
class PendingMFATokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "is_expired")
    readonly_fields = ("created_at",)
    search_fields = ("user__username",)
