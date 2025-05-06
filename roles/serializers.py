from rest_framework import serializers
from .models import (
    Permission, Role, UserRole,
    Policy, PolicyRule,
)

# RBAC serializers

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = "__all__"

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ("id", "user", "role", "assigned_at")
        read_only_fields = ("assigned_at",)

# Policy serializers

class PolicyRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyRule
        fields = ("resource", "access_level")

class PolicySerializer(serializers.ModelSerializer):
    rules = PolicyRuleSerializer(many=True)

    class Meta:
        model = Policy
        fields = ("id", "name", "description", "applies_to", "rules")

    def create(self, validated_data):
        rules_data = validated_data.pop("rules")
        policy = Policy.objects.create(**validated_data)
        for rule in rules_data:
            PolicyRule.objects.create(policy=policy, **rule)
        return policy
