# order_service/app/tests.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Order, Cart, CartItem
from unittest.mock import patch
import json

class OrderViewSetTests(APITestCase):
    def setUp(self):
        self.user = type('User', (), {'id': 1, 'roles': ['user']})()
        self.client.force_authenticate(user=self.user)

    def test_create_order(self):
        url = reverse('order-list')
        data = {
            'customer_id': 1,
            'items': [{'product_id': 1, 'quantity': 2, 'price': 10.00}]
        }
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {'id': 1}
            response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_from_cart(self):
        Cart.objects.create(customer_id=1)
        CartItem.objects.create(cart_id=1, product_id=1, quantity=2, price=10.00)
        url = reverse('order-from-cart')
        with patch('requests.get') as mock_get, patch('requests.post') as mock_post:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {'id': 1}
            mock_post.return_value.status_code = 201
            response = self.client.post(url, {'address': '123 Test St'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(CartItem.objects.count(), 0)  # Кошик очищено

class CartViewSetTests(APITestCase):
    def setUp(self):
        self.user = type('User', (), {'id': 1, 'roles': ['user']})()
        self.client.force_authenticate(user=self.user)
        self.cart = Cart.objects.create(customer_id=1)

    def test_create_cart(self):
        url = reverse('cart-list')
        data = {'customer_id': 1}
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {'id': 1}
            response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 2)

    def test_add_item_to_cart(self):
        url = reverse('cart-add', kwargs={'pk': self.cart.id})
        data = {'product_id': 1, 'quantity': 2, 'price': 10.00}
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {'id': 1, 'price': 10.00}
            response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_remove_item_from_cart(self):
        CartItem.objects.create(cart=self.cart, product_id=1, quantity=2, price=10.00)
        url = reverse('cart-remove', kwargs={'pk': self.cart.id})
        data = {'item_id': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)

    def test_clear_cart(self):
        CartItem.objects.create(cart=self.cart, product_id=1, quantity=2, price=10.00)
        url = reverse('cart-clear', kwargs={'pk': self.cart.id})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)