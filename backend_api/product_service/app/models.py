#product_service/app/models.py
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

name_validator = RegexValidator(
    regex=r'^(?!-)([A-Za-zА-Яа-яїЇіІєЄґҐ]+)(?<!-)$',
    message="Name may contain only Cyrillic, Latin, or hyphen (not at start/end).",
    code='invalid_name'
)

class Category(models.Model):
    name = models.CharField(max_length=255, validators=[name_validator])
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    category_image = models.URLField(null=True, blank=True)
    category_href = models.SlugField(max_length=255, unique=True, blank=True)
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        indexes = [GinIndex(fields=['search_vector'])]
        db_table = 'category'

    def save(self, *args, **kwargs):
        if not self.category_href:
            self.category_href = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    SALE_TYPE_CHOICES = [('fixed', 'Fixed'), ('auction', 'Auction')]
    name = models.CharField(max_length=255, validators=[name_validator])
    vendor_id = models.PositiveBigIntegerField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    sale_type = models.CharField(max_length=20, choices=SALE_TYPE_CHOICES, default='fixed')
    auction_end_time = models.DateTimeField(null=True, blank=True, db_index=True)
    is_approved = models.BooleanField(default=False, db_index=True)
    rating_count = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    product_href = models.SlugField(max_length=255, unique=True, blank=True)
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        indexes = [GinIndex(fields=['search_vector'])]
        db_table = 'product'

    def save(self, *args, **kwargs):
        if not self.product_href:
            self.product_href = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product_id = models.PositiveBigIntegerField(db_index=True)
    image_url = models.URLField()
    user_id = models.PositiveBigIntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'product_image'

    def __str__(self):
        return f"Image for product {self.product_id}"

class Review(models.Model):
    product_id = models.PositiveBigIntegerField(db_index=True)
    user_id = models.PositiveBigIntegerField(db_index=True)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], db_index=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_approved = models.BooleanField(default=False, db_index=True)

    class Meta:
        db_table = 'review'

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            if self.is_approved:
                try:
                    import requests
                    from django.conf import settings
                    requests.patch(
                        f"{settings.PRODUCT_SERVICE_URL}/products/{self.product_id}/update-rating/",
                        json={'rating_count': Review.objects.filter(product_id=self.product_id, is_approved=True).count()}
                    )
                except requests.RequestException as e:
                    logger.error(f"Failed to update rating for product {self.product_id}: {str(e)}")

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            product_id = self.product_id
            super().delete(*args, **kwargs)
            try:
                import requests
                from django.conf import settings
                requests.patch(
                    f"{settings.PRODUCT_SERVICE_URL}/products/{product_id}/update-rating/",
                    json={'rating_count': Review.objects.filter(product_id=product_id, is_approved=True).count()}
                )
            except requests.RequestException as e:
                logger.error(f"Failed to update rating for product {product_id}: {str(e)}")

    def __str__(self):
        return f"Review for product {self.product_id} by user {self.user_id}"

class AuctionBid(models.Model):
    product_id = models.PositiveBigIntegerField(db_index=True)
    user_id = models.PositiveBigIntegerField(db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'auction_bid'
        unique_together = ['product_id', 'user_id']

    def __str__(self):
        return f"Bid {self.amount} for product {self.product_id} by user {self.user_id}"

class Favorite(models.Model):
    user_id = models.PositiveBigIntegerField(db_index=True)
    product_id = models.PositiveBigIntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'favorite'
        unique_together = ['user_id', 'product_id']

    def __str__(self):
        return f"Favorite product {self.product_id} for user {self.user_id}"