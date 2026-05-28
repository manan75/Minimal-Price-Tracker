# tracker/serializers.py

from rest_framework import serializers
from .models import Product, PriceHistory


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['id', 'price', 'scraped_at']


class ProductSerializer(serializers.ModelSerializer):
    latest_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'url',
            'name',
            'site',
            'is_active',
            'latest_price',
            'last_checked_at',
            'created_at',
        ]
        # These are set by the system, not the user
        read_only_fields = ['name', 'site', 'last_checked_at', 'created_at']

    def get_latest_price(self, obj):
        return obj.latest_price()


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Separate serializer for creation.
    User only needs to provide the URL — nothing else.
    """
    class Meta:
        model = Product
        fields = ['url']

    def validate_url(self, value):
        # Normalize: strip trailing slash for consistency
        return value.rstrip('/')