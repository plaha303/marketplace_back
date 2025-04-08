from drf_spectacular.utils import extend_schema, OpenApiExample
from django.utils.timezone import now
from rest_framework import viewsets, permissions, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model

from .models import Product, Order, Cart
from .serializers import (ProductSerializer, OrderSerializer, UserSerializer,
                          RegisterSerializer, PasswordResetRequestSerializer,
                          PasswordResetConfirmSerializer, VerifyEmailSerializer, LoginSerializer,
                          CartSerializer, CartRemoveSerializer)

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
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data.get("email")
        code = serializer.validated_data.get("code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"success": False, "errors": {"email": ["Користувача не знайдено"]}}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_code != code:
            return Response({"success": False, "errors": {"code": ["Невірний код"]}}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_expires_at and now() > user.verification_expires_at:
            user.delete()
            return Response({"success": False, "errors": {"code": ["Код прострочений"]}}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.is_active = True
        user.verification_code = None
        user.verification_expires_at = None
        user.save()

        return Response({"success": true}, status=status.HTTP_200_OK)


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"success": True, "message": "Лист для скидання пароля відправлено на email."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save(uidb64=uidb64, token=token)
            return Response({"success": True, "message": "Пароль успішно змінено."}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"success": False, "errors": {"detail": [str(e)]}}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
class CartAddView(generics.GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            # Перевірка запасу
            if product.stock < quantity:
                return Response(
                    {"success": False, "errors": {"quantity": ["Недостатньо товару на складі"]}},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                new_quantity = cart_item.quantity + quantity
                if product.stock < new_quantity:
                    return Response(
                        {"success": False, "errors": {"quantity": ["Недостатньо товару на складі"]}},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                cart_item.quantity = new_quantity
                cart_item.save()
            return Response(
                {"success": True, "message": "Товар додано до кошика"},
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
        
class CartRemoveView(generics.GenericAPIView):
    serializer_class = CartRemoveSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity_to_remove = serializer.validated_data.get('quantity', 1)  # За замовчуванням 1
            try:
                cart_item = Cart.objects.get(user=request.user, product=product)
                if cart_item.quantity > quantity_to_remove:
                    cart_item.quantity -= quantity_to_remove
                    cart_item.save()
                    return Response(
                        {"success": True, "message": f"Кількість товару зменшено на {quantity_to_remove}"},
                        status=status.HTTP_200_OK
                    )
                else:
                    cart_item.delete()
                    return Response(
                        {"success": True, "message": "Товар видалено з кошика"},
                        status=status.HTTP_200_OK
                    )
            except Cart.DoesNotExist:
                return Response(
                    {"success": False, "errors": {"product": ["Товар не знайдено в кошику"]}},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
        
class CartListView(generics.GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            cart_items = Cart.objects.filter(user=request.user)
            serializer = self.get_serializer(cart_items, many=True)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "errors": {"detail": [str(e)]}}, status=status.HTTP_400_BAD_REQUEST)
