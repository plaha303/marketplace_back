from django.utils.timezone import now
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer, UserSerializer, RegisterSerializer

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


class VerifyEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

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
