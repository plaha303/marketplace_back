from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
import os
import certifi
import re
from django.utils.timezone import now
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

User = get_user_model()
os.environ['SSL_CERT_FILE'] = certifi.where()

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.ListField(child=serializers.ChoiceField(choices=User.ROLE_CHOICES), required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'surname', 'email', 'roles']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'username', 'surname', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Паролі не збігаються."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class VerifyEmailSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Користувача з таким email не знайдено.")
        return value

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField(min_length=8)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Паролі не збігаються."})
        return data

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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'surname', 'email', 'roles']