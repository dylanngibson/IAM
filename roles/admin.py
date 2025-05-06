from django.contrib import admin
from .models import (
    Role, Permission, RolePermission, UserRole,
    Policy, PolicyRule,
)

# RBAC inlines & admins
class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 1

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    inlines = (RolePermissionInline,)
    search_fields = ("name",)

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "codename", "name")
    search_fields = ("codename", "name")

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "role", "assigned_at")
    autocomplete_fields = ("user", "role")
    readonly_fields = ("assigned_at",)

# Policy admins
class PolicyRuleInline(admin.TabularInline):
    model = PolicyRule
    extra = 1

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    inlines = (PolicyRuleInline,)
    search_fields = ("name",)

@admin.register(PolicyRule)
class PolicyRuleAdmin(admin.ModelAdmin):
    list_display = ("id", "policy", "resource", "access_level")
    autocomplete_fields = ("policy",)
