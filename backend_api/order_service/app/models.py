# order_service/app/models.py
from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]
    customer_id = models.PositiveBigIntegerField(db_index=True)  # Змінено з ForeignKey на ID
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Order #{self.id} by customer {self.customer_id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.PositiveBigIntegerField(db_index=True)  # Змінено з ForeignKey на ID
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"OrderItem for product {self.product_id} in order {self.order.id}"

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    PAYMENT_METHODS = [
        ('card', 'Card'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user_id = models.PositiveBigIntegerField(db_index=True)  # Змінено з ForeignKey на ID
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Payment for order {self.order.id}"

class Shipping(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    shipped_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Shipping for order {self.order.id}"

