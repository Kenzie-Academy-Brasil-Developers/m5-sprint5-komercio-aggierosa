from rest_framework import serializers

from .models import User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "password",
            "email",
            "is_seller",
            "is_active",
        ]
        read_only_fields = ["is_active"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AccountManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["is_active"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
