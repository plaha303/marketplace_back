from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from core.models import Product, Cart, Category, Order, OrderItem, Review, AuctionBid, Favorite, Payment, Shipping
from django.test.utils import override_settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import logging
import json


from django.utils.timezone import now
from datetime import timedelta
logger = logging.getLogger(__name__)
User = get_user_model()


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class APITests(APITestCase):
    def setUp(self):
        """Налаштування тестових даних."""
        self.client = APIClient(enforce_csrf_checks=False)

        # Створюємо категорію
        self.category = Category.objects.create(name="Test Category", category_href="test-category")

        # Створюємо користувачів
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='TestUser',
            surname='User',
            password='testpass123',
            roles=['user'],
            is_active=True,
            is_verified=True
        )
        self.admin = User.objects.create_user(
            email='admin@example.com',
            username='Admin',
            surname='Admin',
            password='adminpass123',
            roles=['admin'],
            is_active=True,
            is_verified=True
        )

        # Створюємо продукт
        self.product = Product.objects.create(
            vendor=self.user,
            category=self.category,
            name='Test Product',
            price=10.00,
            stock=10,
            sale_type='fixed',
            product_href='test-product'
        )

        # Створюємо елемент кошика
        self.cart_item = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=1
        )

        # Створюємо замовлення
        self.order = Order.objects.create(
            customer=self.user,
            total_amount=10.00,
            status='pending'
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=self.product.price
        )

        logger.debug("setUp completed: user, admin, category, product, cart_item, order created.")

    def test_register(self):
        """Тестує реєстрацію користувача."""
        data = {
            'username': 'NewUser',
            'surname': 'NewSurname',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123'
        }
        url = '/api/auth/register/'
        response = self.client.post(url, data, format='json')
        logger.debug(f"Register response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertFalse(User.objects.get(email='newuser@example.com').is_verified)

    def test_verify_email(self):
        """Тестує підтвердження email."""
        user = User.objects.create_user(
            email='verifyuser@example.com',
            username='VerifyUser',
            password='verify123',
            is_active=False,
            is_verified=False
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = f'/api/auth/verify-email/{uid}/{token}/'
        response = self.client.get(url)
        logger.debug(f"Verify email response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_verified)

    def test_login(self):
        """Тестує вхід користувача."""
        data = {'email': 'testuser@example.com', 'password': 'testpass123'}
        url = '/api/auth/login/'
        response = self.client.post(url, data, format='json')
        logger.debug(f"Login response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('access', response.data)
        self.assertIn('refresh_token', response.cookies)

    def test_add_to_cart(self):
        self.client.force_authenticate(user=self.user)
        data = {'product': self.product.id, 'quantity': 2}
        url = '/api/cart/add/'
        logger.debug(f"Sending POST to {url} with data: {data}")
        response = self.client.post(url, data, format='json')
        logger.debug(f"Add to cart response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        cart_item = Cart.objects.get(user=self.user, product=self.product)
        self.assertEqual(cart_item.quantity, 3, "Кількість: 1 (setUp) + 2")

    def test_remove_from_cart(self):
        """Тестує видалення продукту з кошика."""
        self.client.force_authenticate(user=self.user)
        data = {'product': self.product.id}
        url = '/api/cart/remove/'
        response = self.client.post(url, data, format='json', HTTP_CONTENT_TYPE='application/json')
        logger.debug(f"Remove from cart response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertFalse(Cart.objects.filter(user=self.user, product=self.product).exists())

    def test_cart_list(self):
        """Тестує отримання списку елементів кошика."""
        self.client.force_authenticate(user=self.user)
        url = '/api/cart/'
        response = self.client.get(url)
        logger.debug(f"Cart list response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(len(response.data['data']), 1)

    def test_create_product(self):
        """Тестує створення продукту."""
        self.client.force_authenticate(user=self.user)
        data = {
            'category': self.category.id,
            'name': 'New Product',
            'price': 20.00,
            'stock': 5,
            'sale_type': 'fixed'
        }
        url = '/api/products/'
        response = self.client.post(url, data, format='json')
        logger.debug(f"Create product response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name='New Product').exists())

    def test_create_order(self):
        """Тестує створення замовлення."""
        self.client.force_authenticate(user=self.user)
        data = {'total_amount': 10.00}
        url = '/api/orders/'
        response = self.client.post(url, data, format='json')
        logger.debug(f"Create order response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertTrue(Order.objects.filter(customer=self.user, total_amount=10.00).exists())

    def test_create_review(self):
        """Тестує створення відгуку."""
        self.client.force_authenticate(user=self.user)
        data = {'product': self.product.id, 'rating': 5, 'comment': 'Great product!'}
        url = '/api/reviews/'
        response = self.client.post(url, data, format='json')
        logger.debug(f"Create review response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Review.objects.filter(product=self.product, user=self.user).exists())

    def test_create_auction_bid(self):
        """Тестує створення ставки на аукціон."""
        auction_product = Product.objects.create(
            vendor=self.user,
            category=self.category,
            name='Auction Product',
            start_price=10.00,
            sale_type='auction',
            auction_end_time=now() + timedelta(days=1),
            stock=1
        )
        self.client.force_authenticate(user=self.user)
        data = {'product': auction_product.id, 'amount': 15.00}
        url = '/api/auction-bids/'
        response = self.client.post(url, data, format='json')
        logger.debug(f"Create auction bid response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AuctionBid.objects.filter(product=auction_product, user=self.user).exists())

    def test_create_favorite(self):
        """Тестує створення обраного продукту."""
        self.client.force_authenticate(user=self.user)
        data = {'product': self.product.id}
        url = '/api/favorites/'
        response = self.client.post(url, data, format='json')
        logger.debug(f"Create favorite response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Favorite.objects.filter(user=self.user, product=self.product).exists())

    def test_create_category(self):
        """Тестує створення категорії."""
        self.client.force_authenticate(user=self.admin)
        data = {'name': 'New Category'}
        url = '/api/categories/'
        response = self.client.post(url, data, format='json')
        logger.debug(f"Create category response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name='New Category').exists())

    def test_create_payment(self):
        """Тестує створення платежу."""
        self.client.force_authenticate(user=self.user)
        data = {'order': self.order.id, 'amount': 10.00, 'payment_method': 'bank_transfer'}
        url = '/api/payments/'
        response = self.client.post(url, data, format='json')
        logger.debug(f"Create payment response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Payment.objects.filter(order=self.order, user=self.user).exists())

    def test_create_shipping(self):
        """Тестує створення доставки."""
        self.order.status = 'paid'
        self.order.save()
        self.client.force_authenticate(user=self.user)
        data = {
            'order': self.order.id,
            'recipient_name': 'Test User',
            'address': '123 Test St',
            'city': 'Test City',
            'postal_code': '12345',
            'country': 'Test Country'
        }
        url = '/api/shipping/'
        response = self.client.post(url, data, format='json')
        logger.debug(f"Create shipping response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Shipping.objects.filter(order=self.order).exists())

    def test_user_profile(self):
        """Тестує отримання профілю користувача."""
        self.client.force_authenticate(user=self.user)
        url = '/api/user/'
        response = self.client.get(url)
        logger.debug(f"User profile response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['email'], 'testuser@example.com')

    def test_password_reset_request(self):
        """Тестує запит на скидання пароля."""
        data = {'email': 'testuser@example.com'}
        url = '/api/auth/password-reset/'
        response = self.client.post(url, data, format='json')
        logger.debug(f"Password reset request response: {response.status_code}, {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])