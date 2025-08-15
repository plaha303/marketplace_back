import random
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.timezone import now, timedelta
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify
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
    order_id = models.PositiveBigIntegerField(null=True, blank=True, db_index=True)
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')
    error = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return f"EmailLog for order #{self.order_id if self.order_id else 'unknown'} - {self.status}"

    class Meta:
        verbose_name = 'Email Log'
        verbose_name_plural = 'Email Logs'