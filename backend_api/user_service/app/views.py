from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework import viewsets, permissions, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django_filters.rest_framework import DjangoFilterBackend
from .filters import UserFilter
from django.contrib.auth import get_user_model
from django.conf import settings
from .permissions import HasRolePermission
from .serializers import (
    UserSerializer, RegisterSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer, VerifyEmailSerializer, LoginSerializer,
    ResendVerificationCodeSerializer, UserProfileSerializer
)
from rest_framework import status
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
import logging
from rest_framework.pagination import PageNumberPagination
from django.db import DatabaseError

logger = logging.getLogger(__name__)
User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "success": True,
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "prev": self.get_previous_link(),
            "results": data
        })

class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={200: {'description': 'Service is healthy'}},
        description="Health check endpoint for user_service"
    )
    def get(self, request):
        return Response({"status": "healthy"}, status=status.HTTP_200_OK)


class OrderInfoView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Order information"}, status=status.HTTP_200_OK)



class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: RegisterSerializer,
            400: {'description': 'Invalid data'},
        },
        description="Register a new user and send a verification email"
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                user = serializer.save()
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                user.verification_token_created_at = now()
                user.save()
                verification_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}"

                from django.core.mail import send_mail
                send_mail(
                    'Підтвердження email',
                    f'Вітаємо, {user.username}!\n\n'
                    f'Будь ласка, перейдіть за посиланням для підтвердження вашого email: {verification_url}\n'
                    f'Посилання дійсне протягом 1 години.\n',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                logger.info(f"Verification email sent to {user.email} for user {user.id}")
                return Response(
                    {"success": True, "message": "Реєстрація успішна. Перевірте вашу пошту для підтвердження."},
                    status=status.HTTP_201_CREATED
                )
        except Exception as e:
            logger.error(f"Error during registration for email {request.data.get('email')}: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )

class VerifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='uidb64', type=str, location=OpenApiParameter.PATH),
            OpenApiParameter(name='token', type=str, location=OpenApiParameter.PATH),
        ],
        responses={
            200: {'description': 'Email verified successfully'},
            400: {'description': 'Invalid or expired token'},
        },
        description="Verify user email with token"
    )
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            logger.error(f"Invalid uidb64: {uidb64} for email verification")
            return Response(
                {"success": False, "errors": {"detail": "Недійсне посилання для підтвердження."}},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.is_verified:
            logger.info(f"User {user.id} email already verified")
            return Response(
                {"success": True, "message": "Email вже підтверджений."},
                status=status.HTTP_200_OK
            )

        if default_token_generator.check_token(user, token):
            if user.verification_token_created_at and (now() - user.verification_token_created_at) <= timedelta(hours=1):
                user.is_verified = True
                user.verification_token_created_at = None
                user.save()
                logger.info(f"Email verified for user {user.id}")
                return Response(
                    {"success": True, "message": "Email успішно підтверджений."},
                    status=status.HTTP_200_OK
                )
            else:
                logger.warning(f"Expired token for user {user.id}")
                return Response(
                    {"success": False, "errors": {"detail": "Посилання для підтвердження прострочене."}},
                    status=status.HTTP_400_BAD_REQUEST
                )
        logger.error(f"Invalid token for user {user.id}")
        return Response(
            {"success": False, "errors": {"detail": "Недійсне посилання для підтвердження."}},
            status=status.HTTP_400_BAD_REQUEST
        )

class ResendVerificationCodeView(GenericAPIView):
    serializer_class = ResendVerificationCodeSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=ResendVerificationCodeSerializer,
        responses={
            200: {'description': 'Verification email resent'},
            400: {'description': 'Invalid email or already verified'},
        },
        description="Resend verification email to user"
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
            logger.info(f"Verification email resent to {user.email} for user {user.id}")
            return Response(
                {"success": True, "message": "Новий код підтвердження надіслано на ваш email."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error resending verification email for {request.data.get('email')}: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: {'description': 'Login successful'},
            400: {'description': 'Invalid credentials or unverified email'},
        },
        description="Authenticate user and return JWT tokens"
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                logger.warning(f"Invalid password for user {email}")
                return Response(
                    {"success": False, "errors": {"detail": "Невірний пароль."}},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not user.is_verified:
                logger.warning(f"Unverified email login attempt for {email}")
                return Response(
                    {"success": False, "errors": {"detail": "Email не підтверджений."}},
                    status=status.HTTP_400_BAD_REQUEST
                )
            refresh = RefreshToken.for_user(user)
            logger.info(f"User {user.id} logged in successfully")
            return Response({
                "success": True,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.error(f"Login attempt with non-existent email: {email}")
            return Response(
                {"success": False, "errors": {"detail": "Користувача з таким email не знайдено."}},
                status=status.HTTP_400_BAD_REQUEST
            )

class CustomTokenRefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        responses={
            200: {'description': 'Token refreshed successfully'},
            401: {'description': 'Invalid refresh token'},
        },
        description="Refresh JWT access token using refresh token"
    )
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            logger.error("No refresh token provided")
            return Response(
                {"success": False, "errors": {"detail": "Refresh token is required."}},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            logger.info("Token refreshed successfully")
            return Response({
                "success": True,
                "access": access_token
            }, status=status.HTTP_200_OK)
        except TokenError as e:
            logger.error(f"Invalid refresh token: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_401_UNAUTHORIZED
            )

class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={
            200: {'description': 'Password reset email sent'},
            400: {'description': 'Invalid email'},
        },
        description="Request password reset email"
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"{settings.FRONTEND_URL}/password-reset-confirm/{uid}/{token}"
            from django.core.mail import send_mail
            send_mail(
                'Скидання пароля',
                f'Вітаємо, {user.username}!\n\n'
                f'Перейдіть за посиланням для скидання пароля: {reset_url}\n'
                f'Посилання дійсне протягом 1 години.\n',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            logger.info(f"Password reset email sent to {user.email} for user {user.id}")
            return Response(
                {"success": True, "message": "Посилання для скидання пароля надіслано на ваш email."},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            logger.error(f"Password reset requested for non-existent email: {email}")
            return Response(
                {"success": False, "errors": {"detail": "Користувача з таким email не знайдено."}},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error sending password reset email for {email}: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )

class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='uidb64', type=str, location=OpenApiParameter.PATH),
            OpenApiParameter(name='token', type=str, location=OpenApiParameter.PATH),
        ],
        request=PasswordResetConfirmSerializer,
        responses={
            200: {'description': 'Password reset successfully'},
            400: {'description': 'Invalid or expired token'},
        },
        description="Confirm password reset with token and set new password"
    )
    def post(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            logger.error(f"Invalid uidb64: {uidb64} for password reset")
            return Response(
                {"success": False, "errors": {"detail": "Недійсне посилання для скидання пароля."}},
                status=status.HTTP_400_BAD_REQUEST
            )

        if default_token_generator.check_token(user, token):
            user.set_password(serializer.validated_data['password'])
            user.save()
            logger.info(f"Password reset for user {user.id}")
            return Response(
                {"success": True, "message": "Пароль успішно скинуто."},
                status=status.HTTP_200_OK
            )
        logger.error(f"Invalid token for password reset for user {user.id}")
        return Response(
            {"success": False, "errors": {"detail": "Недійсне посилання для скидання пароля."}},
            status=status.HTTP_400_BAD_REQUEST
        )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: {'description': 'Logout successful'},
            400: {'description': 'Invalid request'},
        },
        description="Logout user and blacklist refresh token"
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                logger.error("No refresh token provided for logout")
                return Response(
                    {"success": False, "errors": {"detail": "Refresh token is required."}},
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"User {request.user.id} logged out successfully")
            return Response(
                {"success": True, "message": "Успішний вихід із системи."},
                status=status.HTTP_200_OK
            )
        except TokenError as e:
            logger.error(f"Invalid refresh token for logout: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserProfileView(GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: UserProfileSerializer,
            401: {'description': 'Unauthorized'},
        },
        description="Retrieve or update authenticated user's profile"
    )
    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"User {request.user.id} updated profile")
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['admin']
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    pagination_class = StandardResultsSetPagination

    def perform_update(self, serializer):
        serializer.save()
        logger.info(f"User {self.request.user.id} updated user {serializer.instance.id}")

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f"User {self.request.user.id} created user {serializer.instance.id}")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == request.user:
            logger.error(f"User {request.user.id} attempted to delete own account")
            return Response(
                {"success": False, "errors": {"detail": "Ви не можете видалити власний обліковий запис."}},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        logger.info(f"User {request.user.id} deleted user {instance.id}")
        return Response({"success": True, "message": "Користувача видалено."}, status=status.HTTP_204_NO_CONTENT)