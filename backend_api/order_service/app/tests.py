# order_service/app/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Order

class OrderViewSetTests(APITestCase):
    def setUp(self):
        self.user = {'id': 1, 'roles': ['user']}  # Мок користувача
        self.client.force_authenticate(user=self.user)

    def test_create_order(self):
        url = reverse('order-list')
        data = {
            'customer_id': 1,
            'items': [{'product_id': 1, 'quantity': 2, 'price': 10.00}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
