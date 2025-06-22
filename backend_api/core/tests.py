from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from concurrent.futures import ThreadPoolExecutor
from .models import Category, Product, Cart

User = get_user_model()

class OrderTests(APITestCase):
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
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Test Category', category_href='test-category')
        self.product = Product.objects.create(
            vendor=self.user,
            category=self.category,
            name='Test Product',
            price=10.00,
            stock=1,  # Ліміт 1 одиниця
            product_href='test-product'
        )
        # Кошик для користувача з цим товаром
        self.cart_item = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

    def create_order(self, client):
        # Відправляємо POST із необхідними даними
        data = {
            "cart_id": self.cart_item.id  # або інші поля, які потрібні твоєму API для створення замовлення
        }
        response = client.post(reverse('order-list'), data=data, format='json')
        return response

    def test_concurrent_order_creation(self):
        client1 = APIClient()
        client2 = APIClient()
        client1.force_authenticate(user=self.user)
        client2.force_authenticate(user=self.user)

        with ThreadPoolExecutor(max_workers=2) as executor:
            future1 = executor.submit(self.create_order, client1)
            future2 = executor.submit(self.create_order, client2)
            response1 = future1.result()
            response2 = future2.result()

        # Порахувати скільки замовлень створено успішно
        success_count = sum(1 for r in [response1, response2] if r.status_code == status.HTTP_201_CREATED)

        self.assertEqual(success_count, 1, "Only one order should be created due to stock limit")

        # Оновлюємо дані товару
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 0, "Stock should be reduced to 0")



class CoreAppTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Test@1234',
            surname='TestSurname',
            roles=['user'],
            is_verified=False,
            is_active=False
        )

    def test_verify_email_expired_token(self):
        user = User.objects.create_user(
            username='verifyuser',
            email='verify@example.com',
            password='Test@1234',
            surname='VerifySurname',
            is_active=False,
            is_verified=False,
            verification_token_created_at=now() - timedelta(hours=2)  # Токен створений 2 години тому, застарілий
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = reverse('verify-email', args=[uid, token])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Посилання для підтвердження застаріло', response.data.get('errors', {}).get('non_field_errors', [''])[0])

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
        response = self.client.post(reverse('resend-verification-code'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        # Перевіряємо, що час створення токена оновився (менше 60 секунд тому)
        self.assertTrue((now() - user.verification_token_created_at).total_seconds() < 60)
