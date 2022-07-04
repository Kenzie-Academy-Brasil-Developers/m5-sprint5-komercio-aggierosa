from rest_framework import serializers

from .models import Product
from Users.serializer import AccountSerializer


class ProductCreateSerializer(serializers.ModelSerializer):
    seller = AccountSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "descripton",
            "price",
            "quantity",
            "is_active",
            "seller_id",
            "seller",
        ]
        read_only_fields = ["is_active"]
        extra_kwargs = {"quantity": {"min_value": 0}}


class ProductListSerializer(serializers.ModelSerializer):
    seller = AccountSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ["description", "price", "quantity", "is_active", "seller_id"]
