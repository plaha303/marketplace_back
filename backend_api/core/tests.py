from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from core.models import Product, Cart, Order, User
from django.utils.timezone import now, timedelta
from django.core import mail

User = get_user_model()

class ProductViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = User.objects.create_user(
            username='vendor',
            email='vendor@example.com',
            password='pass',
            role='vendor'
        )
        self.vendor.groups.add(Group.objects.get_or_create(name='Vendors')[0])

        self.customer = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='pass',
            role='customer'
        )
        self.customer.groups.add(Group.objects.get_or_create(name='Customers')[0])

        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='pass',
            role='admin'
        )
        self.admin.groups.add(Group.objects.get_or_create(name='Admins')[0])

        self.product = Product.objects.create(
            vendor=self.vendor, name='Test Product', price=100, stock=10
        )

    def test_vendor_can_create_product(self):
        self.client.force_authenticate(self.vendor)
        response = self.client.post('/api/products/', {'name': 'New Product', 'price': 200, 'stock': 5})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 2)

    def test_customer_cannot_create_product(self):
        self.client.force_authenticate(self.customer)
        response = self.client.post('/api/products/', {'name': 'New Product', 'price': 200, 'stock': 5})
        self.assertEqual(response.status_code, 403)

    def test_vendor_cannot_edit_other_product(self):
        other_vendor = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='pass',
            role='vendor'
        )
        other_vendor.groups.add(Group.objects.get_or_create(name='Vendors')[0])
        other_product = Product.objects.create(
            vendor=other_vendor, name='Other Product', price=300, stock=5
        )
        self.client.force_authenticate(self.vendor)
        response = self.client.put(f'/api/products/{other_product.id}/', {'name': 'Edited', 'price': 400, 'stock': 5})
        self.assertEqual(response.status_code, 403)

    def test_admin_can_delete_any_product(self):
        self.client.force_authenticate(self.admin)
        response = self.client.delete(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            role='customer',
            is_verified=True,
            is_active=True
        )
        self.user.groups.add(Group.objects.get_or_create(name='Customers')[0])

    def test_successful_login(self):
        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_failed_login_wrong_password(self):
        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('errors', response.data)

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_successful_registration(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Password123',
            'password2': 'Password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['success'])
        user = User.objects.get(email='newuser@example.com')
        self.assertFalse(user.is_verified)
        self.assertFalse(user.is_active)
        self.assertIsNotNone(user.verification_code)
        self.assertIsNotNone(user.verification_expires_at)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Підтвердження реєстрації')
        self.assertIn(f'Ваш код підтвердження: {user.verification_code}', email.body)
        self.assertNotIn('http://localhost:8000/api/auth/activate/', email.body)

    def test_registration_password_mismatch(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Password123',
            'password2': 'Different123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('non_field_errors', response.data['errors'])
        self.assertEqual(response.data['errors']['non_field_errors'], ['Паролі не співпадають'])

    def test_registration_duplicate_email(self):
        User.objects.create_user(
            username='existing',
            email='newuser@example.com',
            password='Password123'
        )
        response = self.client.post('/api/auth/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Password123',
            'password2': 'Password123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('email', response.data['errors'])

class VerifyEmailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            role='customer',
            is_verified=False,
            is_active=False,
            verification_code='123456',
            verification_expires_at=now() + timedelta(hours=1)
        )

    def test_successful_verification(self):
        response = self.client.post('/api/auth/verify-email/', {
            'email': 'test@example.com',
            'verification_code': '123456'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        user = User.objects.get(email='test@example.com')
        self.assertTrue(user.is_verified)
        self.assertTrue(user.is_active)
        self.assertIsNone(user.verification_code)
        self.assertIsNone(user.verification_expires_at)

    def test_invalid_code(self):
        response = self.client.post('/api/auth/verify-email/', {
            'email': 'test@example.com',
            'verification_code': '999999'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('non_field_errors', response.data['errors'])
        self.assertEqual(response.data['errors']['non_field_errors'], ['Неправильний код підтвердження.'])

    def test_expired_code(self):
        self.user.verification_expires_at = now() - timedelta(hours=1)
        self.user.save()
        response = self.client.post('/api/auth/verify-email/', {
            'email': 'test@example.com',
            'verification_code': '123456'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('non_field_errors', response.data['errors'])
        self.assertEqual(response.data['errors']['non_field_errors'], ['Код підтвердження прострочений.'])

    def test_non_existent_email(self):
        response = self.client.post('/api/auth/verify-email/', {
            'email': 'nonexistent@example.com',
            'verification_code': '123456'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('non_field_errors', response.data['errors'])
        self.assertEqual(response.data['errors']['non_field_errors'], ['Користувач із таким email не існує.'])

class ResendVerificationCodeViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            role='customer',
            is_verified=False,
            is_active=False,
            verification_code='123456',
            verification_expires_at=now() + timedelta(hours=1)
        )

    def test_successful_resend_code(self):
        response = self.client.post('/api/auth/resend-verification-code/', {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['message'], 'Новий код підтвердження відправлено!')
        user = User.objects.get(email='test@example.com')
        self.assertNotEqual(user.verification_code, '123456')  # Код змінився
        self.assertTrue(user.verification_expires_at > now())
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Новий код підтвердження')
        self.assertIn(f'Ваш новий код підтвердження: {user.verification_code}', email.body)
        self.assertNotIn('http://localhost:8000/api/auth/activate/', email.body)

    def test_resend_code_already_verified(self):
        self.user.is_verified = True
        self.user.save()
        response = self.client.post('/api/auth/resend-verification-code/', {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('email', response.data['errors'])
        self.assertEqual(response.data['errors']['email'], ['Email вже підтверджений.'])

    def test_resend_code_non_existent_email(self):
        response = self.client.post('/api/auth/resend-verification-code/', {
            'email': 'nonexistent@example.com'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('email', response.data['errors'])
        self.assertEqual(response.data['errors']['email'], ['Користувача з таким email не знайдено.'])

class ActivateEmailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            role='customer',
            is_verified=False,
            is_active=False
        )

    def test_activate_endpoint_not_found(self):
        response = self.client.get('/api/auth/activate/dummyuid/dummytoken/')
        self.assertEqual(response.status_code, 404)

class CartAddViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='pass',
            role='customer'
        )
        self.customer.groups.add(Group.objects.get_or_create(name='Customers')[0])
        self.vendor = User.objects.create_user(
            username='vendor',
            email='vendor@example.com',
            password='pass',
            role='vendor'
        )
        self.product = Product.objects.create(
            vendor=self.vendor, name='Test Product', price=100, stock=10
        )

    def test_add_to_cart_success(self):
        self.client.force_authenticate(self.customer)
        response = self.client.post('/api/cart/add/', {
            'product': self.product.id,
            'quantity': 2
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['success'])
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.first().quantity, 2)

    def test_add_to_cart_insufficient_stock(self):
        self.client.force_authenticate(self.customer)
        response = self.client.post('/api/cart/add/', {
            'product': self.product.id,
            'quantity': 15
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('quantity', response.data['errors'])

class OrderViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='pass',
            role='customer'
        )
        self.customer.groups.add(Group.objects.get_or_create(name='Customers')[0])
        self.vendor = User.objects.create_user(
            username='vendor',
            email='vendor@example.com',
            password='pass',
            role='vendor'
        )
        self.product = Product.objects.create(
            vendor=self.vendor, name='Test Product', price=100, stock=10
        )
        self.cart_item = Cart.objects.create(
            user=self.customer, product=self.product, quantity=2
        )

    def test_create_order_success(self):
        self.client.force_authenticate(self.customer)
        response = self.client.post('/api/orders/', {})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['success'])
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.total_amount, 200)  # 2 * 100
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(Cart.objects.count(), 0)  # Кошик очищений

    def test_create_order_empty_cart(self):
        Cart.objects.all().delete()
        self.client.force_authenticate(self.customer)
        response = self.client.post('/api/orders/', {})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('cart', response.data['errors'])
class CategoryViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='pass',
            role='admin'
        )
        self.admin.groups.add(Group.objects.get_or_create(name='Admins')[0])
        self.category = Category.objects.create(
            name='Home Products',
            category_href='home-products',
            category_image='https://example.com/sample.jpg'  # Тестовий URL
        )

    def test_retrieve_category_by_href(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get('/home-products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['category_href'], 'home-products')
        self.assertEqual(response.data['data']['category_image'], 'https://example.com/sample.jpg')

    def test_create_category_without_image(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post('/api/categories/', {
            'name': 'New Category'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.last().category_href, 'new-category')
        self.assertIsNone(Category.objects.last().category_image)  # Перевіряємо, що зображення не вказано

class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_successful_registration(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'newuser',
            'surname': 'Smith',
            'email': 'newuser@example.com',
            'password': 'Password123',
            'password_confirm': 'Password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['success'])
        user = User.objects.get(email='newuser@example.com')
        self.assertEqual(user.surname, 'Smith')  # Перевіряємо surname
        self.assertFalse(user.is_verified)
        self.assertFalse(user.is_active)
        self.assertIsNotNone(user.verification_code)
        self.assertIsNotNone(user.verification_expires_at)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Підтвердження реєстрації')
        self.assertIn(f'Ваш код підтвердження: {user.verification_code}', email.body)
        self.assertNotIn('http://localhost:8000/api/auth/activate/', email.body)

    def test_registration_password_mismatch(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'newuser',
            'surname': 'Smith',
            'email': 'newuser@example.com',
            'password': 'Password123',
            'password_confirm': 'Different123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('password_confirm', response.data['errors'])
        self.assertEqual(response.data['errors']['password_confirm'], ['Паролі не співпадають'])

    def test_registration_duplicate_email(self):
        User.objects.create_user(
            username='existing',
            surname='Doe',
            email='newuser@example.com',
            password='Password123'
        )
        response = self.client.post('/api/auth/register/', {
            'username': 'newuser',
            'surname': 'Smith',
            'email': 'newuser@example.com',
            'password': 'Password123',
            'password_confirm': 'Password123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertIn('email', response.data['errors'])

    def test_registration_without_surname(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'Password123',
            'password_confirm': 'Password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['success'])
        user = User.objects.get(email='newuser@example.com')
        self.assertIsNone(user.surname)  # Перевіряємо, що surname може бути null