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
        self.admin = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='Admin@1234',
            surname='AdminSurname',
            roles=['admin'],
            is_verified=True,
            is_active=True
        )
        self.category = Category.objects.create(name='Electronics', category_href='electronics')
        self.product = Product.objects.create(
            vendor=self.user,
            category=self.category,
            name='Test Product',
            description='Test Description',
            sale_type='fixed',
            price=100.00,
            stock=10,
            product_href='test-product'
        )

        self.admin = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='Admin@1234',
            surname='AdminSurname',
            roles=['admin'],
            is_verified=True,
            is_active=True
        )
        self.category = Category.objects.create(name='Electronics', category_href='electronics')
        self.product = Product.objects.create(
            vendor=self.user,
            category=self.category,
            name='Test Product',
            description='Test Description',
            sale_type='fixed',
            price=100.00,
            stock=10,
            product_href='test-product'
        )

    # Model Tests
    def test_user_model_str(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_user_default_role(self):
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='Test@1234',
            surname='NewSurname'
        )
        self.assertEqual(new_user.roles, ['user'])

    def test_category_unique_href(self):
        category = Category.objects.create(name='Electronics 2')
        self.assertTrue(category.category_href.startswith('electronics-2'))

    def test_product_unique_href(self):
        product = Product.objects.create(
            vendor=self.user,
            category=self.category,
            name='Test Product 2',
            price=50.00,
            stock=5
        )
        self.assertTrue(product.product_href.startswith('test-product-2'))

    def test_product_image_str(self):
        image = ProductImage.objects.create(product=self.product, image_url='http://example.com/image.jpg')
        self.assertEqual(str(image), f"Image for {self.product.name}")

    def test_cart_str(self):
        cart = Cart.objects.create(user=self.user, product=self.product, quantity=2)
        self.assertEqual(str(cart), f"2 of {self.product.name} in {self.user.username}'s cart")

    def test_order_str(self):
        order = Order.objects.create(customer=self.user, total_amount=200.00, status='pending')
        self.assertEqual(str(order), f"Order #{order.id} by {self.user.username} - pending")

    def test_order_item_str(self):
        order = Order.objects.create(customer=self.user, total_amount=200.00)
        item = OrderItem.objects.create(order=order, product=self.product, quantity=2, price=100.00)
        self.assertEqual(str(item), f"2 x {self.product.name} in order #{order.id}")

    def test_payment_str(self):
        order = Order.objects.create(customer=self.user, total_amount=200.00)
        payment = Payment.objects.create(order=order, user=self.user, amount=200.00, payment_method='paypal')
        self.assertEqual(str(payment), f"Payment for order #{order.id} - pending")

    def test_shipping_str(self):
        order = Order.objects.create(customer=self.user, total_amount=200.00)
        shipping = Shipping.objects.create(
            order=order,
            recipient_name='Test User',
            address='123 Test St',
            city='Test City',
            postal_code='12345',
            country='Test Country'
        )
        self.assertEqual(str(shipping), f"Shipping for order #{order.id}")

    # Serializer Tests
    def test_register_serializer_valid(self):
        data = {
            'username': 'newuser2',
            'surname': 'NewSurname',
            'email': 'new2@example.com',
            'password': 'Test@1234',
            'password_confirm': 'Test@1234'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_register_serializer_password_mismatch(self):
        data = {
            'username': 'newuser3',
            'surname': 'NewSurname',
            'email': 'new3@example.com',
            'password': 'Test@1234',
            'password_confirm': 'Test@1235'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password_confirm', serializer.errors)

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(serializer.data['username'], 'testuser')

    def test_product_serializer_valid(self):
        data = {
            'category': self.category.id,
            'name': 'New Product',
            'description': 'New Description',
            'sale_type': 'fixed',
            'price': 150.00,
            'stock': 5
        }
        serializer = ProductSerializer(data=data, context={'request': type('Request', (), {'user': self.user})()})
        self.assertTrue(serializer.is_valid())

    def test_product_serializer_invalid_price(self):
        data = {
            'category': self.category.id,
            'name': 'New Product',
            'description': 'New Description',
            'sale_type': 'fixed',
            'stock': 5
        }
        serializer = ProductSerializer(data=data, context={'request': type('Request', (), {'user': self.user})()})
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_cart_serializer_valid(self):
        data = {'product': self.product.id, 'quantity': 2}
        serializer = CartSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_cart_serializer_invalid_quantity(self):
        data = {'product': self.product.id, 'quantity': 0}
        serializer = CartSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    # View Tests
    def test_register_view(self):
        data = {
            'username': 'newuser4',
            'surname': 'NewSurname',
            'email': 'new4@example.com',
            'password': 'Test@1234',
            'password_confirm': 'Test@1234'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='new4@example.com').exists())

    def test_verify_email_view(self):
        user = User.objects.create_user(
            username='verifyuser',
            email='verify@example.com',
            password='Test@1234',
            surname='VerifySurname',
            is_active=False,
            is_verified=False
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        response = self.client.get(reverse('verify-email', args=[uid, token]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.is_verified)
        self.assertTrue(user.is_active)

    def test_login_view(self):
        data = {'email': 'test@example.com', 'password': 'Test@1234'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_view_invalid_credentials(self):
        data = {'email': 'test@example.com', 'password': 'Wrong@1234'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_reset_request(self):
        data = {'email': 'test@example.com'}
        response = self.client.post(reverse('password_reset'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_confirm(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        data = {'new_password': 'New@1234', 'confirm_password': 'New@1234'}
        response = self.client.post(reverse('password_reset_confirm', args=[uid, token]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('New@1234'))

    def test_resend_verification_code(self):
        user = User.objects.create_user(
            username='verifyuser2',
            email='verify2@example.com',
            password='Test@1234',
            surname='VerifySurname',
            is_active=False,
            is_verified=False
        )
        data = {'email': 'verify2@example.com'}
        response = self.client.post(reverse('resend-verification-code'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_list_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # SAFE_METHODS allowed

    def test_product_create(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'category': self.category.id,
            'name': 'New Product',
            'description': 'New Description',
            'sale_type': 'fixed',
            'price': 150.00,
            'stock': 5
        }
        response = self.client.post(reverse('product-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_retrieve_by_href(self):
        response = self.client.get(reverse('product-detail-by-href', args=['electronics', 'test-product']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cart_add(self):
        self.client.force_authenticate(user=self.user)
        data = {'product': self.product.id, 'quantity': 2}
        response = self.client.post(reverse('cart-add'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Cart.objects.filter(user=self.user, product=self.product, quantity=2).exists())

    def test_cart_remove(self):
        Cart.objects.create(user=self.user, product=self.product, quantity=3)
        self.client.force_authenticate(user=self.user)
        data = {'product': self.product.id}
        response = self.client.post(reverse('cart-remove'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Cart.objects.filter(user=self.user, product=self.product).exists())

    def test_cart_list(self):
        Cart.objects.create(user=self.user, product=self.product, quantity=2)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('cart-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_order_create(self):
        Cart.objects.create(user=self.user, product=self.product, quantity=2)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('order-list'), {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Order.objects.filter(customer=self.user).exists())

    def test_review_create(self):
        self.client.force_authenticate(user=self.user)
        data = {'product': self.product.id, 'rating': 4, 'comment': 'Great product!'}
        response = self.client.post(reverse('review-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auction_bid_create(self):
        auction_product = Product.objects.create(
            vendor=self.user,
            category=self.category,
            name='Auction Product',
            sale_type='auction',
            start_price=50.00,
            auction_end_time=now() + timedelta(days=1),
            product_href='auction-product'
        )
        self.client.force_authenticate(user=self.user)
        data = {'product': auction_product.id, 'amount': 60.00}
        response = self.client.post(reverse('auction-bid-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_favorite_create(self):
        self.client.force_authenticate(user=self.user)
        data = {'product': self.product.id}
        response = self.client.post(reverse('favorite-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_category_create_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {'name': 'New Category', 'category_href': 'new-category'}
        response = self.client.post(reverse('category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_payment_create(self):
        order = Order.objects.create(customer=self.user, total_amount=200.00)
        self.client.force_authenticate(user=self.user)
        data = {'order': order.id, 'amount': 200.00, 'payment_method': 'paypal'}
        response = self.client.post(reverse('payment-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_shipping_create(self):
        order = Order.objects.create(customer=self.user, total_amount=200.00)
        self.client.force_authenticate(user=self.user)
        data = {
            'order': order.id,
            'recipient_name': 'Test User',
            'address': '123 Test St',
            'city': 'Test City',
            'postal_code': '12345',
            'country': 'Test Country'
        }
        response = self.client.post(reverse('shipping-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_profile_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['username'], 'testuser')

    # Permission Tests
    def test_has_role_permission_safe_method(self):
        permission = HasRolePermission()
        request = type('Request', (), {'method': 'GET', 'user': self.user})()
        view = type('View', (), {'allowed_roles': ['admin']})()
        self.assertTrue(permission.has_permission(request, view))

    def test_has_role_permission_non_safe_admin(self):
        permission = HasRolePermission()
        request = type('Request', (), {'method': 'POST', 'user': self.admin})()
        view = type('View', (), {'allowed_roles': ['admin']})()
        self.assertTrue(permission.has_permission(request, view))

    def test_has_role_permission_non_safe_user(self):
        permission = HasRolePermission()
        request = type('Request', (), {'method': 'POST', 'user': self.user})()
        view = type('View', (), {'allowed_roles': ['admin']})()
        self.assertFalse(permission.has_permission(request, view))

    def test_has_object_permission_owner(self):
        permission = HasRolePermission()
        request = type('Request', (), {'method': 'PUT', 'user': self.user})()
        view = type('View', (), {'allowed_roles': ['user']})()
        obj = type('Obj', (), {'vendor': self.user})()
        self.assertTrue(permission.has_object_permission(request, view, obj))

    def test_has_object_permission_non_owner(self):
        permission = HasRolePermission()
        request = type('Request', (), {'method': 'PUT', 'user': self.user})()
        view = type('View', (), {'allowed_roles': ['user']})()
        obj = type('Obj', (), {'vendor': self.admin})()
        self.assertFalse(permission.has_object_permission(request, view, obj))

    # Filter Tests
    def test_product_filter_in_stock(self):
        Product.objects.create(
            vendor=self.user,
            category=self.category,
            name='Out of Stock',
            price=50.00,
            stock=0,
            product_href='out-of-stock'
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('product-list'), {'in_stock': True})
        data = response.data.get('results', response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Test Product')

    def test_order_filter_status(self):
        Order.objects.create(customer=self.user, total_amount=200.00, status='paid')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('order-list'), {'status': 'pending'})
        data = response.data.get('results', response.data)
        self.assertEqual(len(data), 0)
