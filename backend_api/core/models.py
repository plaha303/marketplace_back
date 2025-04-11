import random

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now, timedelta


class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer', db_index=True)
    is_verified = models.BooleanField(default=False, db_index=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_expires_at = models.DateTimeField(null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_users',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_users_permissions',
        blank=True
    )

    def generate_verification_code(self):
        self.verification_code = str(random.randint(100000, 999999))
        self.verification_expires_at = now() + timedelta(hours=1)
        self.save()
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Спочатку зберігаємо користувача
        group_name = {
            'customer': 'Customers',
            'vendor': 'Vendors',
            'admin': 'Admins'
        }.get(self.role)
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            if not self.groups.filter(name=group_name).exists():
                self.groups.add(group)
    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Product(models.Model):
    SALE_TYPE_CHOICES = [
        ('fixed', 'Fixed Price'),
        ('auction', 'Auction'),
    ]
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    sale_type = models.CharField(max_length=10, choices=SALE_TYPE_CHOICES, default='fixed', db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    start_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    auction_end_time = models.DateTimeField(null=True, blank=True, db_index=True)
    stock = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()

    def __str__(self):
        return f"Image for {self.product.name}"


class AuctionBid(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Bid of {self.amount} by {self.user.username} on {self.product.name}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.user.username}'s cart"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order #{self.order.id}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='bank_transfer')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Payment for order #{self.order.id} - {self.status}"


class Shipping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping')
    recipient_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=50, null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True, db_index=True)

    def __str__(self):
        return f"Shipping for order #{self.order.id}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(db_index=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s favorite for {self.product.name}"
        

