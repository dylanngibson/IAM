from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
    date_hierarchy = "date_joined"
