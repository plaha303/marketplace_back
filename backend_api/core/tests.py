import uuid
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import Category, Product, ProductImage, Cart, Order, OrderItem, Payment, Shipping, Review, AuctionBid, Favorite
from .serializers import RegisterSerializer, UserSerializer, ProductSerializer, CartSerializer, OrderSerializer, ReviewSerializer
from .permissions import HasRolePermission
import json

User = get_user_model()

# tests.py
from django.utils.timezone import now, timedelta

class CoreAppTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Test@1234',
            surname='TestSurname',
            roles=['user'],
            is_verified=True,
            is_active=True
        )

    def test_verify_email_expired_token(self):
        user = User.objects.create_user(
            username='verifyuser',
            email='verify@example.com',
            password='Test@1234',
            surname='VerifySurname',
            is_active=False,
            is_verified=False,
            verification_token_created_at=now() - timedelta(hours=2)  # Токен застарілий
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        response = self.client.get(reverse('verify-email', args=[uid, token]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Посилання для підтвердження застаріло', response.data['errors']['non_field_errors'][0])

    def test_resend_verification_code_updates_timestamp(self):
        user = User.objects.create_user(
            username='verifyuser2',
            email='verify2@example.com',
            password='Test@1234',
            surname='VerifySurname',
            is_active=False,
            is_verified=False,
            verification_token_created_at=now() - timedelta(hours=2)
        )
        data = {'email': 'verify2@example.com'}
        response = self.client.post(reverse('resend-verification-code'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue((now() - user.verification_token_created_at).total_seconds() < 60)  # Час оновлено