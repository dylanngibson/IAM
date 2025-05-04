from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Attribute, UserAttribute, ResourceAttribute


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "key", "value")
    search_fields = ("key", "value")


class UserAttributeInline(admin.TabularInline):
    model = UserAttribute
    extra = 1
    autocomplete_fields = ("attribute",)


class ResourceAttributeInline(GenericTabularInline):
    model = ResourceAttribute
    extra = 1
    autocomplete_fields = ("attribute",)


# Optionally add the inline to your User admin:
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin
# admin.site.unregister(get_user_model())
# @admin.register(get_user_model())
# class CustomUserAdmin(UserAdmin):
#     inlines = (UserAttributeInline,)
