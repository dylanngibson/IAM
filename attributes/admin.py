# admin.py
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
