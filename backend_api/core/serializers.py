from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from .models import Product, ProductImage, Order, OrderItem, Category, Cart, Review, AuctionBid, Favorite, Payment, Shipping, PlatformReview
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
import os
import certifi
import re
from django.utils.timezone import now
from datetime import timedelta
from rest_framework import serializers

from django.db.models import Avg
import logging
logger = logging.getLogger(__name__)

User = get_user_model()
os.environ['SSL_CERT_FILE'] = certifi.where()

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.ListField(child=serializers.ChoiceField(choices=User.ROLE_CHOICES), required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'surname', 'email', 'roles']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'category_image', 'category_href']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'image', 'user_id']

class CategoryImageUploadSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    image = serializers.ImageField()

    def validate(self, data):
        category_id = data.get('category_id')
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            logger.error(f"Category with ID {category_id} not found")
            raise serializers.ValidationError({"category_id": "Категорія не знайдена"})

        image = data.get('image')
        if image.size > 32 * 1024 * 1024:
            raise serializers.ValidationError({"image": "Розмір зображення не може перевищувати 32MB"})
        if not image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            raise serializers.ValidationError({"image": "Дозволені формати: JPG, JPEG, PNG, GIF"})

        return data

class ProductImageUploadSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    image = serializers.ImageField()

    def validate(self, data):
        product_id = data.get('product_id')
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            logger.error(f"Product with ID {product_id} not found")
            raise serializers.ValidationError({"product_id": "Продукт не знайдений"})

        image = data.get('image')
        if image.size > 32 * 1024 * 1024:
            raise serializers.ValidationError({"image": "Розмір зображення не може перевищувати 32MB"})
        if not image.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            raise serializers.ValidationError({"image": "Дозволені формати: JPG, JPEG, PNG, GIF"})

        return data

class ProductSerializer(serializers.ModelSerializer):
    vendor = UserSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    isAvailable = serializers.SerializerMethodField()
    reviews_count = serializers.IntegerField(read_only=True, source='rating_count')
    productId = serializers.IntegerField(source='id')
    categoryId = serializers.IntegerField(source='category.id', allow_null=True)
    rating = serializers.SerializerMethodField()
    discount_tag = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['productId', 'vendor', 'categoryId', 'name', 'description',
                  'sale_type', 'price', 'discount_price', 'start_price', 'auction_end_time',
                  'stock', 'created_at', 'images', 'product_href', 'isAvailable', 'reviews_count', 'rating', 'discount_tag']

    def get_isAvailable(self, obj):
        return obj.is_available()

    def get_rating(self, obj):
        # Обчислюємо середній рейтинг на основі всіх відгуків продукту
        average = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        # Повертаємо середній рейтинг з округленням до 2 знаків після коми, або null, якщо відгуків немає
        return round(average, 2) if average is not None else None

    def get_discount_tag(self, obj):
        if obj.sale_type == 'fixed' and obj.discount_price is not None and obj.price is not None and obj.price > 0:
            discount_percentage = round(((obj.price - obj.discount_price) / obj.price) * 100)
            return f"{discount_percentage}%"
        return None

    def validate_categoryId(self, value):
        if value is not None:
            try:
                Category.objects.get(id=value)
            except Category.DoesNotExist:
                raise serializers.ValidationError({"categoryId": "Категорія з таким ID не існує."})
        return value

    def validate(self, data):
        sale_type = data.get('sale_type', self.instance.sale_type if self.instance else 'fixed')
        price = data.get('price', self.instance.price if self.instance else None)
        discount_price = data.get('discount_price', self.instance.discount_price if self.instance else None)

        if sale_type == 'fixed' and price is None:
            raise serializers.ValidationError({"price": "Для типу продажу 'fixed' ціна обов’язкова."})
        if sale_type == 'fixed' and discount_price is not None:
            if price is None:
                raise serializers.ValidationError({"price": "Ціна обов’язкова, якщо вказана знижка."})
            if discount_price > price:
                raise serializers.ValidationError({"discount_price": "Знижена ціна не може бути більшою за звичайну ціну."})
        if sale_type == 'auction' and discount_price is not None:
            raise serializers.ValidationError({"discount_price": "Знижена ціна не підтримується для аукціонів."})
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['vendor'] = request.user
        return super().create(validated_data)

class OrderItemSerializer(serializers.ModelSerializer):
    productId = serializers.IntegerField(source='product.id', allow_null=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'productId', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'total_amount', 'status', 'created_at', 'updated_at', 'items']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['customer'] = request.user
        return super().create(validated_data)

name_validator = RegexValidator(
    regex=r'^(?!-)([A-Za-zА-Яа-яїЇіІєЄґҐ]+)(?<!-)$',
    message="Ім'я та прізвище можуть містити лише кирилицю, латиницю, дефіс (не на початку чи в кінці).",
    code='invalid_name'
)

email_local_part_validator = RegexValidator(
    regex=r'^(?![\.])([A-Za-z0-9._%+-]+)(?<!\.)$',
    message="Локальна частина email може містити латиницю, цифри, спеціальні символи, крапку (не на початку чи в кінці).",
    code='invalid_email_local_part'
)

email_domain_validator = RegexValidator(
    regex=r'^(?!-|\.)([A-Za-z0-9-]+)(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$',
    message="Доменна частина email може містити латиницю, цифри, дефіс (не на початку чи в кінці), крапку.",
    code='invalid_email_domain'
)

password_validator = RegexValidator(
    regex=r'^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};:"\\\',.<>?/]{8,16}$',
    message="Пароль може містити латиницю, цифри, спеціальні символи та мати довжину від 8 до 16 символів.",
    code='invalid_password'
)

class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True, min_length=8, max_length=16, validators=[password_validator])

    class Meta:
        model = User
        fields = ['username', 'surname', 'email', 'password', 'password_confirm']
        extra_kwargs = {
            'username': {'validators': [name_validator], 'min_length': 1, 'max_length': 50},
            'surname': {'validators': [name_validator], 'min_length': 1, 'max_length': 50},
            'email': {'min_length': 1, 'max_length': 70},
            'password': {'write_only': True, 'validators': [password_validator], 'min_length': 8, 'max_length': 16},
        }

    def validate_email(self, value):
        if len(value) > 70:
            raise ValidationError("Загальна довжина email не може перевищувати 70 символів.")
        try:
            local_part, domain = value.split('@')
        except ValueError:
            raise ValidationError("Email повинен містити символ '@'.")
        if len(local_part) < 1 or len(local_part) > 35:
            raise ValidationError("Локальна частина email повинна мати від 1 до 35 символів.")
        if not re.match(r'^(?![\.])([A-Za-z0-9._%+-]+)(?<!\.)$', local_part):
            raise ValidationError("Локальна частина email містить некоректні символи або крапки на початку/кінці.")
        if re.search(r'\.{2,}', local_part):
            raise ValidationError("Локальна частина email не може містити послідовні крапки.")
        if len(domain) < 3 or len(domain) > 35:
            raise ValidationError("Доменна частина email повинна мати від 3 до 35 символів.")
        if not re.match(r'^(?!-|\.)([A-Za-z0-9-]+)(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$', domain):
            raise ValidationError("Доменна частина email містить некоректні символи або крапки/дефіси на початку/кінці.")
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise ValidationError({'password_confirm': 'Паролі не співпадають.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            surname=validated_data.get('surname'),
            roles=['user']
        )
        user.is_active = False
        user.is_verified = False

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        user.verification_token_created_at = now()
        user.save()
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"

        send_mail(
            'Підтвердження реєстрації',
            f'Вітаємо, {user.username} ({user.email})!\n\n'
            f'Будь ласка, перейдіть за посиланням для підтвердження вашого email: {verification_url}\n'
            f'Посилання дійсне протягом 1 години.\n',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return user
class PlatformReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformReview
        fields = ['id', 'avatar', 'name', 'surname', 'city', 'rating', 'review_text', 'created_at']

class VerifyEmailSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, data):
        uidb64 = data.get('uidb64')
        token = data.get('token')
        logger.info(f"Attempting to verify email with uidb64: {uidb64}")

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            logger.error(f"Invalid uidb64: {uidb64}")
            raise serializers.ValidationError({"non_field_errors": ["Невірне посилання для підтвердження."]})

        if not default_token_generator.check_token(user, token):
            logger.error(f"Invalid or expired token for user {user.email}")
            raise serializers.ValidationError({"non_field_errors": ["Невірне посилання для підтвердження."]})

        if user.is_verified:
            logger.info(f"Email {user.email} already verified")
            raise serializers.ValidationError({"non_field_errors": ["Email вже підтверджений."]})

        if user.verification_token_created_at and (now() - user.verification_token_created_at) > timedelta(hours=1):
            logger.warning(f"Verification token expired for user {user.email}")
            raise serializers.ValidationError({"non_field_errors": ["Посилання для підтвердження застаріло."]})

        logger.info(f"Verification successful for user {user.email}")
        return data

    def save(self):
        uidb64 = self.validated_data['uidb64']
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user.is_active = True
        user.is_verified = True
        user.save()
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise ValidationError('Користувача з таким email не знайдено.')
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"{settings.FRONTEND_URL}/password-reset-confirm/{uid}/{token}/"

        send_mail(
            subject="Скидання пароля",
            message=f"Щоб скинути пароль, перейдіть за посиланням: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8, max_length=16, validators=[password_validator])
    confirm_password = serializers.CharField(write_only=True, min_length=8, max_length=16, validators=[password_validator])

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise ValidationError("Паролі не співпадають.")
        return data

    def save(self, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise ValidationError("Невірне посилання для скидання пароля.")

        if not default_token_generator.check_token(user, token):
            raise ValidationError("Посилання для скидання пароля недійсне.")

        user.set_password(self.validated_data['new_password'])
        user.save()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        User = get_user_model()

        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    raise serializers.ValidationError(
                        {'email': ['Невірний email або пароль'], 'password': ['Невірний email або пароль']})
                if not user.is_active or not user.is_verified:
                    raise serializers.ValidationError({'email': ['Обліковий запис не активний або не підтверджений']})
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    {'email': ['Невірний email або пароль'], 'password': ['Невірний email або пароль']})
        else:
            raise serializers.ValidationError({'email': ['Це поле обов’язкове'], 'password': ['Це поле обов’язкове']})

        data['user'] = user
        return data

class CartSerializer(serializers.ModelSerializer):
    productId = serializers.IntegerField(source='product.id')

    class Meta:
        model = Cart
        fields = ['productId', 'quantity']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Кількість повинна бути більшою за 0.")
        return value

    def validate(self, data):
        product_id = data.get('product').id
        quantity = data.get('quantity')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"productId": "Продукт не знайдений."})
        if product.stock < quantity:
            raise serializers.ValidationError({"quantity": "Недостатньо товару в наявності."})
        return data

class CartRemoveSerializer(serializers.Serializer):
    productId = serializers.IntegerField(source='product.id')

    def validate_productId(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"productId": "Продукт не знайдений."})
        return value

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    productId = serializers.IntegerField(source='product.id')

    class Meta:
        model = Review
        fields = ['id', 'productId', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Рейтинг має бути від 0 до 5.")
        return value

class AuctionBidSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    productId = serializers.IntegerField(source='product.id')

    class Meta:
        model = AuctionBid
        fields = ['id', 'productId', 'user', 'amount', 'created_at']
        read_only_fields = ['user', 'created_at']

class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    productId = serializers.IntegerField(source='product.id')

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'productId']
        read_only_fields = ['user']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'user', 'amount', 'payment_method', 'status', 'created_at']

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['id', 'order', 'recipient_name', 'address', 'city', 'postal_code', 'country', 'tracking_number',
                  'shipped_at']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'surname', 'email', 'roles']

class ResendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        email = data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": ["Користувача з таким email не знайдено."]})

        if user.is_verified:
            raise serializers.ValidationError({"email": ["Email вже підтверджений."]})

        return data

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        user.verification_token_created_at = now()
        user.save()
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}"

        send_mail(
            'Новий код підтвердження',
            f'Вітаємо, {user.username} ({user.email})!\n\n'
            f'Будь ласка, перейдіть за посиланням для підтвердження вашого email: {verification_url}\n'
            f'Посилання дійсне протягом 1 години.\n',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return user

class SearchResultSerializer(serializers.Serializer):
    type = serializers.CharField()  # Тип результату: 'user', 'category', 'product'
    id = serializers.IntegerField()
    name = serializers.CharField()
    details = serializers.SerializerMethodField()
    relevance = serializers.FloatField()  # Ранг релевантності

    def get_details(self, obj):
        if obj['type'] == 'user':
            user = User.objects.get(id=obj['id'])
            return UserSerializer(user).data
        elif obj['type'] == 'category':
            category = Category.objects.get(id=obj['id'])
            return CategorySerializer(category).data
        elif obj['type'] == 'product':
            product = Product.objects.get(id=obj['id'])
            return ProductSerializer(product, context=self.context).data
        return {}