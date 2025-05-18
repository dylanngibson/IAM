# serializers.py
from rest_framework import serializers
from .models import Attribute, UserAttribute, ResourceAttribute

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = "__all__"

class UserAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only=True)
    attribute_id = serializers.PrimaryKeyRelatedField(
        queryset=Attribute.objects.all(),
        write_only=True,
        source="attribute"
    )

    class Meta:
        model = UserAttribute
        fields = ("id", "user", "attribute", "attribute_id")
        read_only_fields = ("user",)

class ResourceAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only=True)
    attribute_id = serializers.PrimaryKeyRelatedField(
        queryset=Attribute.objects.all(),
        write_only=True,
        source="attribute"
    )

    class Meta:
        model = ResourceAttribute
        fields = ("id", "attribute", "attribute_id")
