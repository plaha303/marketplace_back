from rest_framework import serializers
from .models import Payment
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order_id', 'amount', 'status', 'created_at', 'payment_method']
        read_only_fields = ['created_at', 'status']

    def validate_order_id(self, value):
        try:
            response = requests.get(f"{settings.ORDER_SERVICE_URL}/orders/{value}", timeout=5)
            response.raise_for_status()
            order_data = response.json()
            self.initial_data['amount'] = order_data['total_amount']  # Оновлюємо суму з замовлення
            return value
        except requests.RequestException as e:
            logger.error(f"Failed to validate order_id {value}: {str(e)}")
            raise serializers.ValidationError("Invalid order_id")