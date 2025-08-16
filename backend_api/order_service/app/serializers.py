# order_service/app/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem, Cart, CartItem
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
            product_data = response.json()
            # Оновлення ціни з product_service
            self.initial_data['price'] = product_data['price']
            return value
        except requests.RequestException as e:
            logger.error(f"Failed to validate product_id {value}: {str(e)}")
            raise serializers.ValidationError("Invalid product_id")

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment_status = serializers.SerializerMethodField()
    shipping_status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'status', 'total_amount', 'created_at', 'items', 'payment_status', 'shipping_status']
        read_only_fields = ['created_at']

    def validate_customer_id(self, value):
        try:
            response = requests.get(f"{settings.USER_SERVICE_URL}/users/{value}", timeout=5)
            response.raise_for_status()
            return value
        except requests.RequestException as e:
            logger.error(f"Failed to validate customer_id {value}: {str(e)}")
            raise serializers.ValidationError("Invalid customer_id")

    def get_payment_status(self, obj):
        try:
            response = requests.get(f"{settings.PAYMENT_SERVICE_URL}/payments/?order_id={obj.id}", timeout=5)
            response.raise_for_status()
            payment_data = response.json()
            return payment_data[0]['status'] if payment_data else 'pending'
        except requests.RequestException as e:
            logger.error(f"Failed to fetch payment status for order {obj.id}: {str(e)}")
            return 'unknown'

    def get_shipping_status(self, obj):
        try:
            response = requests.get(f"{settings.SHIPPING_SERVICE_URL}/shipping/?order_id={obj.id}", timeout=5)
            response.raise_for_status()
            shipping_data = response.json()
            return shipping_data[0]['status'] if shipping_data else 'pending'
        except requests.RequestException as e:
            logger.error(f"Failed to fetch shipping status for order {obj.id}: {str(e)}")
            return 'unknown'

    def validate(self, data):
        return data

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity', 'price']

    def validate_product_id(self, value):
        try:
            response = requests.get(f"{settings.PRODUCT_SERVICE_URL}/products/{value}", timeout=5)
            response.raise_for_status()
            product_data = response.json()
            self.initial_data['price'] = product_data['price']
            return value
        except requests.RequestException as e:
            logger.error(f"Failed to validate product_id {value}: {str(e)}")
            raise serializers.ValidationError("Invalid product_id")

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer_id', 'created_at', 'updated_at', 'items']
        read_only_fields = ['created_at', 'updated_at']

    def validate_customer_id(self, value):
        try:
            response = requests.get(f"{settings.USER_SERVICE_URL}/users/{value}", timeout=5)
            response.raise_for_status()
            return value
        except requests.RequestException as e:
            logger.error(f"Failed to validate customer_id {value}: {str(e)}")
            raise serializers.ValidationError("Invalid customer_id")