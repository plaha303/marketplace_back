from drf_spectacular.utils import extend_schema, OpenApiExample
from django.utils.timezone import now
from rest_framework import viewsets, permissions, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter, OrderFilter, UserFilter, CartFilter, ReviewFilter, AuctionBidFilter, FavoriteFilter, CategoryFilter, PaymentFilter, ShippingFilter

from django.contrib.auth import get_user_model
from .permissions import HasGroupPermission
from .models import Product, Order, Cart, Review, AuctionBid, Favorite, Category, Payment, Shipping
from .serializers import (ProductSerializer, OrderSerializer, UserSerializer,
                          RegisterSerializer, PasswordResetRequestSerializer,
                          PasswordResetConfirmSerializer, VerifyEmailSerializer, LoginSerializer,
                          CartSerializer, ResendVerificationCodeSerializer, OrderItem, CartRemoveSerializer, ReviewSerializer, AuctionBidSerializer, FavoriteSerializer, CategorySerializer, PaymentSerializer, ShippingSerializer, UserProfileSerializer)
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [HasGroupPermission]
    allowed_groups = ['Admins']
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    
    def perform_update(self, serializer):
        # Дозволяємо оновлювати groups тільки адмінам
        serializer.save()

    def perform_create(self, serializer):
        # Переконуємося, що створюємо користувача з правильною групою
        serializer.save()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [HasGroupPermission]
    allowed_groups = ['Vendors', 'Admins']
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [HasGroupPermission]
    allowed_groups = ['Customers', 'Admins']
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):
        if self.request.user.groups.filter(name='Admins').exists():
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)

    def create(self, request, *args, **kwargs):
        # Перевіряємо, чи є товари в кошику
        cart_items = Cart.objects.filter(user=self.request.user)
        if not cart_items.exists():
            return Response({"success": False, "errors": {"cart": "Кошик порожній."}}, status=status.HTTP_400_BAD_REQUEST)

        # Створюємо серіалізатор для замовлення
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Рахуємо загальну суму замовлення
        total_amount = sum(item.product.price * item.quantity for item in cart_items if item.product.price is not None)
        # Зберігаємо замовлення
        order = serializer.save(customer=self.request.user, total_amount=total_amount)

        # Створюємо елементи замовлення (OrderItem) для кожного товару з кошика
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        # Очищаємо кошик після створення замовлення
        cart_items.delete()
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
# Цей рядок треба поміняти: замінити старий perform_create на новий метод create
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
        code = serializer.validated_data.get("verification_code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"success": False, "errors": {"email": ["Користувача не знайдено"]}}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_code != code:
            return Response({"success": False, "errors": {"code": ["Невірний код"]}}, status=status.HTTP_400_BAD_REQUEST)

        if user.verification_expires_at and now() > user.verification_expires_at:
            return Response(
                {"success": False, "errors": {"code": ["Код прострочений. Відправте новий код через /api/auth/resend-verification-code/"]}},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_verified = True
        user.is_active = True
        user.verification_code = None
        user.verification_expires_at = None
        user.save()

        return Response({"success": True}, status=status.HTTP_200_OK)


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"success": True, "message": "Лист для скидання пароля відправлено на email."}, status=status.HTTP_200_OK)

class ResendVerificationCodeView(APIView):
    def post(self, request):
        serializer = ResendVerificationCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"success": True, "data": {"message": "Новий код підтвердження відправлено!"}}, status=status.HTTP_200_OK)


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
        }, status=status.HTTP_400_BAD_REQUEST
        )





class CartAddView(generics.GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [HasGroupPermission]
    allowed_groups = ['Customers']

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
    permission_classes = [HasGroupPermission]
    allowed_groups = ['Customers']

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
    permission_classes = [HasGroupPermission]
    allowed_groups = ['Customers']
    filter_backends = [DjangoFilterBackend]
    filterset_class = CartFilter

    def get(self, request, *args, **kwargs):
        try:
            queryset = Cart.objects.filter(user=request.user)
            # Застосовуємо фільтри
            filterset = self.filterset_class(request.GET, queryset=queryset)
            if not filterset.is_valid():
                return Response({"success": False, "errors": filterset.errors}, status=status.HTTP_400_BAD_REQUEST)
            filtered_queryset = filterset.qs
            serializer = self.get_serializer(filtered_queryset, many=True)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "errors": {"detail": [str(e)]}}, status=status.HTTP_400_BAD_REQUEST)
            
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [HasGroupPermission]
    allowed_groups = ['Customers']
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter
    
class AuctionBidViewSet(viewsets.ModelViewSet):
    queryset = AuctionBid.objects.all()
    serializer_class = AuctionBidSerializer
    permission_classes = [HasGroupPermission]
    allowed_groups = ['Customers']
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuctionBidFilter

    def get_queryset(self):
        return AuctionBid.objects.filter(user=self.request.user)  
        
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [HasGroupPermission]
    allowed_groups = ['Customers']
    filter_backends = [DjangoFilterBackend]
    filterset_class = FavoriteFilter

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
        
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [HasGroupPermission]
    allowed_groups = ['Admins']
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [HasGroupPermission]
    allowed_groups = ['Customers']
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
        
class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [HasGroupPermission]
    allowed_groups = ['Customers']
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShippingFilter

    def get_queryset(self):
        return Shipping.objects.filter(order__customer=self.request.user)
        
class UserProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response({"success": True, "data": serializer.data})

