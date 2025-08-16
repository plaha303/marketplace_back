from django.db import models
from django.core.validators import MinValueValidator
from django.utils.timezone import now

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    order_id = models.PositiveBigIntegerField(db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    payment_method = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'payment'

    def __str__(self):
        return f"Payment #{self.id} for order {self.order_id} ({self.status})"