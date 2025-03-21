from drf_spectacular.utils import extend_schema, OpenApiExample
from django.utils.timezone import now
from rest_framework import viewsets, permissions, status, generics
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

from .models import Product, Order
from .serializers import (ProductSerializer, OrderSerializer, UserSerializer,
                          RegisterSerializer, PasswordResetRequestSerializer,
                          PasswordResetConfirmSerializer, VerifyEmailSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    # @extend_schema(
    #     request=VerifyEmailSerializer,
    #     responses={200: {"message": "Електронна пошта підтверджена"}},
    #     examples=[
    #         OpenApiExample(
    #             name="Приклад успішного запиту",
    #             value={"email": "user@example.com", "code": "123456"},
    #             request_only=True,
    #         )
    #     ],
    # )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get("email")
        code = serializer.validated_data.get("code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Користувача не знайдено"}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_code != code:
            return Response({"error": "Невірний код"}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_expires_at and now() > user.verification_expires_at:
            user.delete()
            return Response({"error": "Код прострочений, зареєструйтеся знову"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.is_active = True
        user.verification_code = None
        user.verification_expires_at = None
        user.save()

        return Response({"message": "Електронна пошта підтверджена"}, status=status.HTTP_200_OK)


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Лист для скидання пароля відправлено на email."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(uidb64=uidb64, token=token)
        return Response({"message": "Пароль успішно змінено."}, status=status.HTTP_200_OK)
