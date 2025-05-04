from django.contrib import admin
from .models import Role, Permission, RolePermission, UserRole


class RolePermissionInline(admin.TabularInline):
    """
    Lets you add/remove permissions directly inside the Role page.
    """
    model = RolePermission
    extra = 1  # how many blank lines to show


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    inlines = (RolePermissionInline,)          # ← replaces filter_horizontal
    search_fields = ("name",)                  # ← satisfies admin.E040


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "codename", "name")
    search_fields = ("codename", "name")


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "role", "assigned_at")
    autocomplete_fields = ("user", "role")     # still works
    readonly_fields = ("assigned_at",)


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "role", "permission")
    autocomplete_fields = ("role", "permission")
