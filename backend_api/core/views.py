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

from .models import Product, Order, Cart, Review, AuctionBid, Favorite, Category, Payment, Shipping
from .serializers import (ProductSerializer, OrderSerializer, UserSerializer,
                          RegisterSerializer, PasswordResetRequestSerializer,
                          PasswordResetConfirmSerializer, VerifyEmailSerializer, LoginSerializer,
                          CartSerializer, CartRemoveSerializer, ReviewSerializer, AuctionBidSerializer, FavoriteSerializer, CategorySerializer, PaymentSerializer, ShippingSerializer, UserProfileSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    
    

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def perform_create(self, serializer):
        if not (self.request.user.groups.filter(name='Vendors').exists() or 
                self.request.user.groups.filter(name='Admins').exists()):
            raise PermissionDenied("Тільки продавці або адміни можуть створювати продукти.")
        serializer.save(vendor=self.request.user)

    def perform_update(self, serializer):
        product = self.get_object()
        
        if self.request.user.groups.filter(name='Admins').exists():
            serializer.save()
        elif (self.request.user.groups.filter(name='Vendors').exists() and 
              product.vendor == self.request.user):
            serializer.save()
        else:
            #403
            raise PermissionDenied("Ви не маєте прав редагувати цей продукт.")

    def perform_destroy(self, instance):
        product = instance
        
        if self.request.user.groups.filter(name='Admins').exists():
            product.delete()
        elif (self.request.user.groups.filter(name='Vendors').exists() and 
              product.vendor == self.request.user):
            product.delete()
        else:
            #403
            raise PermissionDenied("Ви не маєте прав видаляти цей продукт.")


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter
    
class AuctionBidViewSet(viewsets.ModelViewSet):
    queryset = AuctionBid.objects.all()
    serializer_class = AuctionBidSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuctionBidFilter

    def get_queryset(self):
        return AuctionBid.objects.filter(user=self.request.user)  
        
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FavoriteFilter

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
        
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
        
class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [permissions.IsAuthenticated]
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
