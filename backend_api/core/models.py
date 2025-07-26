import random
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.timezone import now, timedelta
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from cloudinary.models import CloudinaryField
from django.utils.text import slugify  # Переносимо імпорт на початок файлу
from pytils.translit import slugify
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.search import SearchVector
from django.db import transaction

name_validator = RegexValidator(
    regex=r'^(?!-)([A-Za-zА-Яа-яїЇіІєЄґҐ]+)(?<!-)$',
    message="Ім'я та прізвище можуть містити лише кирилицю, латиницю, дефіс (не на початку чи в кінці).",
    code='invalid_name'
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, surname, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, surname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('roles', ['admin'])

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, surname, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, validators=[name_validator])
    surname = models.CharField(max_length=50, validators=[name_validator])
    roles = ArrayField(
        models.CharField(max_length=10, choices=ROLE_CHOICES),
        default=list,
        blank=True,
        db_index=True
    )
    is_verified = models.BooleanField(default=False, db_index=True)
    verification_token_created_at = models.DateTimeField(null=True, blank=True)
    search_vector = SearchVectorField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'surname']

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.is_superuser and not self.roles:
                self.roles = ['user']
            super().save(*args, **kwargs)
            User.objects.filter(pk=self.pk).update(
                search_vector=(
                        SearchVector('username', weight='A', config='ukrainian') +
                        SearchVector('surname', weight='B', config='ukrainian')
                )
            )
    class Meta:
        indexes = [
            GinIndex(fields=['search_vector'], name='user_search_idx'),
        ]

    def __str__(self):
        return f"{self.username} (ID: {self.id})"

class EmailLog(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    ]
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, related_name='email_logs')
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')
    error = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(db_index=True)

    def __str__(self):
        return f"EmailLog for order #{self.order.id if self.order else 'unknown'} - {self.status}"

    class Meta:
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Logs'

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, db_index=True)
    category_image = CloudinaryField('image', blank=True, null=True)
    category_href = models.SlugField(max_length=255, unique=True, blank=True)
    search_vector = SearchVectorField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.category_href:
            self.category_href = slugify(self.name)
            if not self.category_href:
                self.category_href = f"category-{self.id or Category.objects.count() + 1}"
            base_href = self.category_href
            counter = 1
            while Category.objects.filter(category_href=self.category_href).exclude(id=self.id).exists():
                self.category_href = f"{base_href}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

        # Після збереження — оновлюємо search_vector
        Category.objects.filter(pk=self.pk).update(
            search_vector=SearchVector('name', weight='A', config='ukrainian')
        )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        indexes = [
            GinIndex(fields=['search_vector'], name='category_search_idx'),
        ]

name_validator = RegexValidator(
    regex=r'^[A-Za-zА-Яа-я0-9\s\-\']+$',
    message="Назва продукту може містити літери, цифри, пробіли, дефіси та одинарні лапки.",
    code='invalid_product_name'
)
class Product(models.Model):
    SALE_TYPE_CHOICES = [
        ('fixed', 'Fixed Price'),
        ('auction', 'Auction'),
    ]

    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, db_index=True, validators=[name_validator])
    description = models.TextField(blank=True)
    sale_type = models.CharField(max_length=10, choices=SALE_TYPE_CHOICES, default='fixed', db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    start_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    auction_end_time = models.DateTimeField(null=True, blank=True, db_index=True)
    stock = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    product_href = models.SlugField(max_length=255, unique=True, blank=True)  #SlugField
    rating_count = models.PositiveIntegerField(default=0, db_index=True)
    search_vector = SearchVectorField(null=True, blank=True)
    is_approved = models.BooleanField(default=False, db_index=True)  # Поле для модерації

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.name.strip():
                raise ValueError("Назва продукту не може бути порожньою.")
            if not self.product_href:
                self.product_href = slugify(self.name)
                if not self.product_href:
                    self.product_href = f"product-{self.id or Product.objects.count() + 1}"
                base_href = self.product_href
                counter = 1
                while Product.objects.filter(product_href=self.product_href).exclude(id=self.id).exists():
                    self.product_href = f"{base_href}-{counter}"
                    counter += 1
            if self.sale_type == 'fixed' and self.discount_price is not None:
                if self.price is None:
                    raise ValueError("Для типу продажу 'fixed' ціна обов’язкова, якщо вказана знижка.")
                if self.discount_price > self.price:
                    raise ValueError("Знижена ціна не може бути більшою за звичайну ціну.")
            if self.sale_type == 'auction' and self.discount_price is not None:
                self.discount_price = None
            super().save(*args, **kwargs)
            Product.objects.filter(pk=self.pk).update(
                search_vector=(
                        SearchVector('name', weight='A', config='ukrainian') +
                        SearchVector('description', weight='B', config='ukrainian')
                )
            )

    def is_available(self):
        return self.stock > 0 and self.is_approved

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector'], name='product_search_idx'),
        ]

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    user_id = models.IntegerField(null=True, blank=True)  # Якщо це поле також є
    image_url = models.URLField(null=True, blank=True)  # Вже має null=True
    image = CloudinaryField('image', null=True, blank=True)  # Додаємо null=True, blank=True

    def __str__(self):
        return f"Image for {self.product.name}"

class AuctionBid(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Bid of {self.amount} by {self.user.username} (ID: {self.user.id}) on {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.user.username} (ID: {self.user.id})'s cart"

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
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username} (ID: {self.customer.id}) - {self.status}"

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
        return f"Payment for order #{self.order.id} by {self.user.username} (ID: {self.user.id}) - {self.status}"

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
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        db_index=True
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_approved = models.BooleanField(default=False, db_index=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.rating_count = self.product.reviews.filter(is_approved=True).count()  # Обновлюємо тільки для схвалених відгуків
        self.product.save(update_fields=['rating_count'])

    def delete(self, *args, **kwargs):
        product = self.product
        super().delete(*args, **kwargs)
        product.rating_count = product.reviews.filter(
            is_approved=True).count()  # Обновлюємо тільки для схвалених відгуків
        product.save(update_fields=['rating_count'])

    def __str__(self):
        return f"Review by {self.user.username} (ID: {self.user.id}) for {self.product.name}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.username} (ID: {self.user.id})'s favorite for {self.product.name}"


class PlatformReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='platform_reviews')
    avatar = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=50, validators=[name_validator])
    surname = models.CharField(max_length=50, validators=[name_validator])
    city = models.CharField(max_length=100)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], db_index=True)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Platform review by {self.name} {self.surname} from {self.city}"