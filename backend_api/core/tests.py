from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from core.models import Product

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