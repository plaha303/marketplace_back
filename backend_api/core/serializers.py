from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from .models import Product, ProductImage, Order, OrderItem, Category, Cart, Review, AuctionBid, Favorite, Payment, Shipping
from django.utils import timezone
from django.utils.crypto import get_random_string
from datetime import timedelta
import os
import certifi

User = get_user_model()
os.environ['SSL_CERT_FILE'] = certifi.where()

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.ListField(child=serializers.CharField(), required=False)  # Для ArrayField
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'roles']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url']

class ProductSerializer(serializers.ModelSerializer):
    vendor = UserSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'vendor', 'category', 'name', 'description',
                  'sale_type', 'price', 'start_price', 'auction_end_time',
                  'stock', 'created_at', 'images']

    def validate(self, data):
        sale_type = data.get('sale_type', self.instance.sale_type if self.instance else 'fixed')
        price = data.get('price', self.instance.price if self.instance else None)
        if sale_type == 'fixed' and price is None:
            raise serializers.ValidationError({"price": "Для типу продажу 'fixed' ціна обов’язкова."})
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['vendor'] = request.user
        return super().create(validated_data)

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'total_amount', 'status', 'created_at', 'items']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['customer'] = request.user
        return super().create(validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Паролі не співпадають')
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.is_verified = False
        user.roles = ['user']
        user.save()
        user.generate_verification_code()

        send_mail(
            'Підтвердження реєстрації',
            f'Вітаємо, {user.username}!\n\n'
            f'Ваш код підтвердження: {user.verification_code} (дійсний 1 годину).\n',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return user

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    verification_code = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        verification_code = data.get('verification_code')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Користувач із таким email не існує.")

        if user.verification_code != verification_code:
            raise serializers.ValidationError("Неправильний код підтвердження.")

        if user.verification_expires_at < timezone.now():
            raise serializers.ValidationError("Код підтвердження прострочений.")

        return data

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        user.is_active = True
        user.verification_code = None
        user.verification_expires_at = None
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
        reset_url = f"localhost:8000/api/auth/password-reset-confirm/{uid}/{token}"

        send_mail(
            subject="Скидання пароля",
            message=f"Щоб скинути пароль, перейдіть за посиланням: {reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

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
                    raise serializers.ValidationError({'email': ['Невірний email або пароль'], 'password': ['Невірний email або пароль']})
                if not user.is_active or not user.is_verified:
                    raise serializers.ValidationError({'email': ['Обліковий запис не активний або не підтверджений']})
            except User.DoesNotExist:
                raise serializers.ValidationError({'email': ['Невірний email або пароль'], 'password': ['Невірний email або пароль']})
        else:
            raise serializers.ValidationError({'email': ['Це поле обов’язкове'], 'password': ['Це поле обов’язкове']})

        data['user'] = user
        return data

class CartSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Cart
        fields = ['product', 'quantity']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Кількість повинна бути більшою за 0.")
        return value

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']
        if product.stock < quantity:
            raise serializers.ValidationError({"quantity": "Недостатньо товару в наявності."})
        return data

class CartRemoveSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Рейтинг має бути від 1 до 5.")
        return value

class AuctionBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionBid
        fields = ['id', 'product', 'user', 'amount', 'created_at']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'user', 'amount', 'payment_method', 'status', 'created_at']

class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = ['id', 'order', 'recipient_name', 'address', 'city', 'postal_code', 'country', 'tracking_number', 'shipped_at']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'roles']

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
        user.verification_code = get_random_string(length=6, allowed_chars='1234567890')
        user.verification_expires_at = timezone.now() + timedelta(minutes=30)
        user.save()

        send_mail(
            'Новий код підтвердження',
            f'Ваш новий код підтвердження: {user.verification_code} (дійсний 30 хвилин).',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return user