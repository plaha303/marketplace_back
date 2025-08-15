# order_service/app/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem, Payment, Shipping
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'quantity', 'price']

    def validate_product_id(self, value):
        try:
            response = requests.get(f"{settings.PRODUCT_SERVICE_URL}/products/{value}", timeout=5)
            response.raise_for_status()
            return value
        except requests.RequestException as e:
            logger.error(f"Failed to validate product_id {value}: {str(e)}")
            raise serializers.ValidationError("Invalid product_id")

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'user_id', 'amount', 'payment_method', 'status', 'created_at']
        read_only_fields = ['created_at']

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['id', 'order', 'recipient_name', 'address', 'city', 'postal_code', 'country', 'tracking_number', 'shipped_at']
        read_only_fields = ['shipped_at']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)
    shipping = ShippingSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'status', 'total_amount', 'created_at', 'items', 'payment', 'shipping']
        read_only_fields = ['created_at']

    def validate_customer_id(self, value):
        try:
            response = requests.get(f"{settings.USER_SERVICE_URL}/users/{value}", timeout=5)
            response.raise_for_status()
            return value
        except requests.RequestException as e:
            logger.error(f"Failed to validate customer_id {value}: {str(e)}")
            raise serializers.ValidationError("Invalid customer_id")

    def validate(self, data):
        # Додаткова валідація, наприклад, перевірка product_id через product_service
        return data

