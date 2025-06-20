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
from .permissions import HasRolePermission
from .models import Product, Order, Cart, Review, AuctionBid, Favorite, Category, Payment, Shipping
from .serializers import (ProductSerializer, OrderSerializer, UserSerializer,
                          RegisterSerializer, PasswordResetRequestSerializer,
                          PasswordResetConfirmSerializer, VerifyEmailSerializer, LoginSerializer,
                          CartSerializer, ResendVerificationCodeSerializer, OrderItem, CartRemoveSerializer,
                          ReviewSerializer, AuctionBidSerializer, FavoriteSerializer, CategorySerializer, PaymentSerializer,
                          ShippingSerializer, UserProfileSerializer)
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['admin']
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def perform_update(self, serializer):
        serializer.save()

    def perform_create(self, serializer):
        serializer.save()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user', 'admin']
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def retrieve_by_href(self, request, category_href=None, product_href=None):
        try:
            product = Product.objects.get(product_href=product_href, category__category_href=category_href)
            serializer = self.get_serializer(product)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"success": False, "errors": {"detail": "Продукт не знайдено"}}, status=status.HTTP_404_NOT_FOUND)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user', 'admin']
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):
        if 'admin' in self.request.user.roles:
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)

    def create(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=self.request.user)
        if not cart_items.exists():
            return Response({"success": False, "errors": {"cart": "Кошик порожній."}},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        total_amount = sum(item.product.price * item.quantity for item in cart_items if item.product.price is not None)
        order = serializer.save(customer=self.request.user, total_amount=total_amount)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart_items.delete()
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        logger.info(f"RegisterView accessed with method: {request.method}")
        logger.info(f"Request headers: {request.headers}")
        logger.info(f"Request data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User registered with email: {request.data.get('email')}")
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        logger.error(f"Registration failed with errors: {serializer.errors}")
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def get(self, request, uidb64, token):
        serializer = self.get_serializer(data={'uidb64': uidb64, 'token': token})
        if not serializer.is_valid():
            errors = serializer.errors
            if "Посилання для підтвердження застаріло" in str(errors):
                errors["non_field_errors"] = [
                    "Посилання для підтвердження застаріло. Надішліть новий код через /auth/resend-verification-code/."]
            return Response({"success": False, "errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer.save()
            return Response({"success": True, "message": "Email успішно підтверджено."}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"success": False, "errors": {"detail": str(e)}}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"success": True, "message": "Лист для скидання пароля відправлено на email."},
                        status=status.HTTP_200_OK)

class ResendVerificationCodeView(APIView):
    def post(self, request):
        serializer = ResendVerificationCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"success": True, "data": {"message": "Новий код підтвердження відправлено!"}},
                        status=status.HTTP_200_OK)

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
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        response_data = {
            'success': True,
            'access': str(refresh.access_token),
        }

        response = Response(response_data, status=status.HTTP_200_OK)
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite='Strict',
            max_age=14 * 24 * 60 * 60,
        )
        return response

class CustomTokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response(
                {"success": False, "errors": {"detail": "Refresh token not provided in cookies"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response(
                {"success": True, "access": access_token},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )

class CartAddView(generics.GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
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
    permission_classes = [HasRolePermission]
    allowed_roles = ['user']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity_to_remove = serializer.validated_data.get('quantity', 1)
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
    permission_classes = [HasRolePermission]
    allowed_roles = ['user']
    filter_backends = [DjangoFilterBackend]
    filterset_class = CartFilter

    def get(self, request, *args, **kwargs):
        try:
            queryset = Cart.objects.filter(user=request.user)
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
    permission_classes = [HasRolePermission]
    allowed_roles = ['user']
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

class AuctionBidViewSet(viewsets.ModelViewSet):
    queryset = AuctionBid.objects.all()
    serializer_class = AuctionBidSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user']
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuctionBidFilter

    def get_queryset(self):
        return AuctionBid.objects.filter(user=self.request.user)

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user']
    filter_backends = [DjangoFilterBackend]
    filterset_class = FavoriteFilter

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['admin']
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

    def retrieve_by_href(self, request, category_href=None):
        try:
            category = Category.objects.get(category_href=category_href)
            serializer = self.get_serializer(category)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"success": False, "errors": {"detail": "Категорію не знайдено"}}, status=status.HTTP_404_NOT_FOUND)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user']
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user']
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