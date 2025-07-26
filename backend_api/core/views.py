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
from .filters import ProductFilter, OrderFilter, UserFilter, CartFilter, ReviewFilter, AuctionBidFilter, FavoriteFilter, CategoryFilter, PaymentFilter, ShippingFilter
from django.contrib.auth import get_user_model
from django.conf import settings
from .permissions import HasRolePermission, ReviewPermission
from .models import Product, Order, Cart, Review, AuctionBid, Favorite, Category, Payment, Shipping, PlatformReview, User
from .serializers import (ProductSerializer, OrderSerializer, UserSerializer,
                          RegisterSerializer, PasswordResetRequestSerializer,
                          PasswordResetConfirmSerializer, VerifyEmailSerializer, LoginSerializer,
                          CartSerializer, ResendVerificationCodeSerializer, OrderItem, CartRemoveSerializer,
                          ReviewSerializer, AuctionBidSerializer, FavoriteSerializer, CategorySerializer, PaymentSerializer,
                          ShippingSerializer, UserProfileSerializer, CategoryImageUploadSerializer, ProductImageUploadSerializer,
                          PlatformReviewSerializer, SearchResultSerializer)
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.db import transaction
from core.tasks import upload_image_to_cloudinary
import logging
from rest_framework.viewsets import ViewSet
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from rest_framework import viewsets, mixins
from django.db.models import Q, Value, CharField, F
from django.db.models.functions import Concat
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from itertools import chain
from django.db import DatabaseError
from rest_framework.viewsets import GenericViewSet

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

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from django.db.models import Count
from django.db import transaction
from .models import Product, Category
from .serializers import ProductSerializer, ProductImageUploadSerializer
from .filters import ProductFilter
from rest_framework.permissions import IsAuthenticated
from .permissions import HasRolePermission
from django_filters.rest_framework import DjangoFilterBackend
import logging

logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user', 'admin']
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend]
    throttle_scope = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            return queryset.filter(stock__gt=0, is_approved=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user, is_approved=False)

    def perform_update(self, serializer):
        try:
            with transaction.atomic():
                instance = Product.objects.select_for_update().get(id=serializer.instance.id)
                if instance.vendor != self.request.user and 'admin' not in self.request.user.roles:
                    logger.warning(f"User {self.request.user.id} attempted to update product {instance.id} without permission")
                    return Response(
                        {"success": False, "errors": {"detail": "Ви не маєте дозволу на редагування цього продукту"}},
                        status=status.HTTP_403_FORBIDDEN
                    )
                if instance.stock < 0:
                    logger.error(f"Invalid stock update for product {instance.id} by user {self.request.user.id}")
                    return Response(
                        {"success": False, "errors": {"stock": ["Запас не може бути від’ємним"]}},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                serializer.save()
                logger.info(f"Product {instance.id} updated by user {self.request.user.id}")
        except Product.DoesNotExist:
            logger.error(f"Product {serializer.instance.id} not found for user {self.request.user.id}")
            return Response(
                {"success": False, "errors": {"detail": "Продукт не знайдено"}},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating product for user {self.request.user.id}: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve_by_href(self, request, category_href=None, product_href=None):
        logger.debug(f"retrieve_by_href called with category_href={category_href}, product_href={product_href}")
        try:
            product = Product.objects.get(product_href=product_href, category__category_href=category_href)
            serializer = self.get_serializer(product)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            logger.error(f"Product not found for category_href={category_href}, product_href={product_href}")
            return Response({"success": False, "errors": {"detail": "Продукт не знайдено"}}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def upload_image(self, request, pk=None):
        product = self.get_object()
        if product.vendor != request.user and 'admin' not in request.user.roles:
            logger.warning(f"User {request.user.id} attempted to upload image for product {product.id} without permission")
            return Response(
                {"success": False, "errors": {"detail": "Ви не маєте дозволу на завантаження зображень для цього продукту"}},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = ProductImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product_id = serializer.validated_data['product_id']
                image = serializer.validated_data['image']
                from core.tasks import upload_image_to_cloudinary
                upload_image_to_cloudinary.delay(
                    model_type='product',
                    instance_id=product_id,
                    user_id=request.user.id,
                    image_data=image.read(),
                    image_name=image.name
                )
                logger.info(f"Image upload task queued for product {product_id} by user {request.user.id}")
                return Response(
                    {"success": True, "data": {"message": "Завантаження зображення розпочато, URL буде збережено асинхронно"}},
                    status=status.HTTP_202_ACCEPTED
                )
            except Exception as e:
                logger.error(f"Error queuing image upload for user {request.user.id}: {str(e)}")
                return Response(
                    {"success": False, "errors": {"detail": str(e)}},
                    status=status.HTTP_400_BAD_REQUEST
                )
        logger.error(f"Invalid product image upload data for user {request.user.id}: {serializer.errors}")
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

class OrderViewSet(viewsets.ModelViewSet):
    throttle_scope = 'orders'
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user', 'admin']
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def list(self, request, *args, **kwargs):
        logger.debug(f"OrderViewSet list called by user {request.user.id if request.user.is_authenticated else 'anonymous'}")
        return super().list(request, *args, **kwargs)

    def perform_update(self, serializer):
        try:
            with transaction.atomic():
                instance = Order.objects.select_for_update().get(id=serializer.instance.id)
                old_status = instance.status
                serializer.save()
                new_status = serializer.validated_data.get('status', instance.status)
                logger.info(f"Order {instance.id} updated by user {self.request.user.id}")

                # Виклик Celery завдання для надсилання email, якщо статус змінився
                if old_status != new_status:
                    from .tasks import send_order_status_update_email
                    send_order_status_update_email.delay(instance.id, new_status)
        except Order.DoesNotExist:
            logger.error(f"Order {serializer.instance.id} not found for user {self.request.user.id}")
            return Response(
                {"success": False, "errors": {"detail": "Замовлення не знайдено"}},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error updating order for user {self.request.user.id}: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_queryset(self):
        logger.debug(f"OrderViewSet get_queryset for user {self.request.user.id if self.request.user.is_authenticated else 'anonymous'}")
        if 'admin' in self.request.user.roles:
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)

    def create(self, request, *args, **kwargs):
        logger.debug(f"OrderViewSet create called by user {request.user.id} with data: {request.data}")
        cart_items = Cart.objects.filter(user=self.request.user)
        if not cart_items.exists():
            logger.warning(f"User {request.user.id} attempted to create order with empty cart")
            return Response({"success": False, "errors": {"cart": "Кошик порожній."}},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                product_ids = [item.product.id for item in cart_items]
                products = Product.objects.select_for_update().filter(id__in=product_ids)
                product_dict = {p.id: p for p in products}

                for item in cart_items:
                    product = product_dict.get(item.product.id)
                    if not product or product.stock < item.quantity:
                        logger.error(f"Insufficient stock for product {item.product.id} for user {request.user.id}")
                        return Response(
                            {"success": False,
                             "errors": {"quantity": f"Недостатньо товару {item.product.name} на складі"}},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                total_amount = sum(
                    item.product.price * item.quantity for item in cart_items if item.product.price is not None)

                order = serializer.save(customer=self.request.user, total_amount=total_amount)

                for item in cart_items:
                    product = product_dict[item.product.id]
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item.quantity,
                        price=product.price
                    )
                    product.stock -= item.quantity
                    product.save()

                cart_items.delete()
                logger.info(f"Order {order.id} created successfully for user {request.user.id}")

            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating order for user {request.user.id}: {str(e)}")
            return Response({"success": False, "errors": {"detail": str(e)}}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    throttle_scope = 'register'
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
    throttle_scope = 'password_reset'
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"success": True, "message": "Лист для скидання пароля відправлено на email."},
                        status=status.HTTP_200_OK)

class ResendVerificationCodeView(APIView):
    throttle_scope = 'resend_code'
    def post(self, request):
        serializer = ResendVerificationCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"success": True, "data": {"message": "Новий код підтвердження відправлено!"}},
                        status=status.HTTP_200_OK)

class PasswordResetConfirmView(GenericAPIView):
    throttle_scope = 'password_reset_confirm'
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
    throttle_scope = 'login'
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        response = Response({
            'success': True,
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)
        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='None',
            max_age=14 * 24 * 60 * 60,
            path='/'
        )
        logger.info(f"User {user.id} logged in, refresh_token set with Partitioned attribute")
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

class CartAddView(GenericAPIView):
    throttle_scope = 'cart_add'
    serializer_class = CartSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user']

    def post(self, request, *args, **kwargs):
        logger.debug(f"CartAddView POST request by user {request.user.id} with data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Invalid cart data for user {request.user.id}: {serializer.errors}")
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        try:
            with transaction.atomic():
                product = Product.objects.select_for_update().get(id=product.id)
                if product.stock < quantity:
                    logger.error(f"Insufficient stock for product {product.id} for user {request.user.id}")
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
                        logger.error(f"Insufficient stock for product {product.id} for user {request.user.id}")
                        return Response(
                            {"success": False, "errors": {"quantity": ["Недостатньо товару на складі"]}},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    cart_item.quantity = new_quantity
                    cart_item.save()

                logger.info(f"Cart updated for user {request.user.id}, product {product.id}, quantity {quantity}")
            return Response(
                {"success": True, "message": "Товар додано до кошика"},
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
        except Product.DoesNotExist:
            logger.error(f"Product {product.id} not found for user {request.user.id}")
            return Response(
                {"success": False, "errors": {"product": ["Товар не знайдено"]}},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error adding to cart for user {request.user.id}: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )

class CartRemoveView(GenericAPIView):
    serializer_class = CartRemoveSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user']

    def post(self, request, *args, **kwargs):
        logger.debug(f"CartRemoveView POST request by user {request.user.id} with data: {request.data}")
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Invalid cart remove data for user {request.user.id}: {serializer.errors}")
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = serializer.validated_data['product']
        quantity_to_remove = serializer.validated_data.get('quantity', 1)

        try:
            with transaction.atomic():
                cart_item = Cart.objects.select_for_update().get(user=request.user, product=product)
                if cart_item.quantity > quantity_to_remove:
                    cart_item.quantity -= quantity_to_remove
                    cart_item.save()
                    logger.info(f"Reduced quantity by {quantity_to_remove} for product {product.id} in cart for user {request.user.id}")
                    return Response(
                        {"success": True, "message": f"Кількість товару зменшено на {quantity_to_remove}"},
                        status=status.HTTP_200_OK
                    )
                else:
                    cart_item.delete()
                    logger.info(f"Removed product {product.id} from cart for user {request.user.id}")
                    return Response(
                        {"success": True, "message": "Товар видалено з кошика"},
                        status=status.HTTP_200_OK
                    )
        except Cart.DoesNotExist:
            logger.error(f"Cart item for product {product.id} not found for user {request.user.id}")
            return Response(
                {"success": False, "errors": {"product": ["Товар не знайдено в кошику"]}},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error removing from cart for user {request.user.id}: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
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


class CategoryImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [HasRolePermission]
    allowed_roles = ['admin']

    def post(self, request, *args, **kwargs):
        logger.debug(f"CategoryImageUploadView POST request by user {request.user.id} with data: {request.data}")
        serializer = CategoryImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                category_id = serializer.validated_data['category_id']
                image = serializer.validated_data['image']
                upload_image_to_cloudinary.delay(
                    model_type='category',
                    instance_id=category_id,
                    user_id=request.user.id,
                    image_data=image.read(),
                    image_name=image.name
                )
                logger.info(f"Image upload task queued for category {category_id} by user {request.user.id}")
                return Response(
                    {
                        "success": True,
                        "data": {"message": "Завантаження зображення розпочато, URL буде збережено асинхронно"}
                    },
                    status=status.HTTP_202_ACCEPTED
                )
            except Exception as e:
                logger.error(f"Error queuing image upload for user {request.user.id}: {str(e)}")
                return Response(
                    {"success": False, "errors": {"detail": str(e)}},
                    status=status.HTTP_400_BAD_REQUEST
                )
        logger.error(f"Invalid category image upload data for user {request.user.id}: {serializer.errors}")
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [HasRolePermission]
    allowed_roles = ['user', 'admin']  # Vendors та адміни

    @extend_schema(
        request={'multipart/form-data': ProductImageUploadSerializer},
        responses={202: None},
        description="Upload an image for a product to ImgBB asynchronously"
    )
    def post(self, request, *args, **kwargs):
        logger.debug(f"ProductImageUploadView POST request by user {request.user.id} with data: {request.data}")
        serializer = ProductImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product_id = serializer.validated_data['product_id']
                image = serializer.validated_data['image']

                # Викликаємо Celery задачу
                upload_image_to_cloudinary(
                    model_type='product',
                    instance_id=product_id,
                    user_id=request.user.id,
                    image_data=image.read(),
                    image_name=image.name
                )
                logger.info(f"Image upload task queued for product {product_id} by user {request.user.id}")
                return Response(
                    {
                        "success": True,
                        "data": {"message": "Завантаження зображення розпочато, URL буде збережено асинхронно"}
                    },
                    status=status.HTTP_202_ACCEPTED
                )
            except Exception as e:
                logger.error(f"Error queuing image upload for user {request.user.id}: {str(e)}")
                return Response(
                    {"success": False, "errors": {"detail": str(e)}},
                    status=status.HTTP_400_BAD_REQUEST
                )
        logger.error(f"Invalid product image upload data for user {request.user.id}: {serializer.errors}")
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

class ReviewViewSet(viewsets.ModelViewSet):
    throttle_scope = 'reviews'
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewPermission]
    allowed_roles = ['user']
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get_queryset(self):
        if 'admin' in self.request.user.roles:
            return Review.objects.all()  # Адміни бачать усі відгуки
        return Review.objects.filter(is_approved=True)  # Звичайні користувачі бачать тільки схвалені відгуки

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Invalid review data for user {request.user.id}: {serializer.errors}")
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                serializer.save(user=self.request.user, is_approved=False)
                logger.info(f"Review created for product {serializer.validated_data['product'].id} by user {request.user.id}")
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating review for user {request.user.id}: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST)

class AuctionBidViewSet(viewsets.ModelViewSet):
    throttle_scope = 'auction_bids'
    queryset = AuctionBid.objects.all()
    serializer_class = AuctionBidSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user']
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuctionBidFilter

    def get_queryset(self):
        return AuctionBid.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Invalid auction bid data for user {request.user.id}: {serializer.errors}")
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = serializer.validated_data['product']
        amount = serializer.validated_data['amount']

        try:
            with transaction.atomic():
                product = Product.objects.select_for_update().get(id=product.id)
                if product.sale_type != 'auction' or product.auction_end_time < now():
                    logger.error(f"Invalid auction for product {product.id} for user {request.user.id}")
                    return Response(
                        {"success": False, "errors": {"product": ["Аукціон завершено або недоступний"]}},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                max_bid = product.bids.order_by('-amount').first()
                min_bid = product.start_price or 0
                if max_bid:
                    min_bid = max_bid.amount

                if amount <= min_bid:
                    logger.error(f"Bid {amount} too low for product {product.id} for user {request.user.id}")
                    return Response(
                        {"success": False, "errors": {"amount": ["Ставка повинна перевищувати поточну максимальну"]}},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                serializer.save(user=self.request.user)
                logger.info(f"Bid {amount} placed on product {product.id} by user {request.user.id}")

            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            logger.error(f"Product {product.id} not found for user {request.user.id}")
            return Response(
                {"success": False, "errors": {"product": ["Товар не знайдено"]}},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error placing bid for user {request.user.id}: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user']
    filter_backends = [DjangoFilterBackend]
    filterset_class = FavoriteFilter

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [HasRolePermission(allowed_roles=['admin'])]

    @extend_schema(
        responses={200: CategorySerializer(many=True)},
        description="Повертає список усіх категорій, доступний для всіх користувачів."
    )
    def list(self, request, *args, **kwargs):
        logger.debug(f"CategoryViewSet list called by user {request.user.id if request.user.is_authenticated else 'anonymous'}")
        return super().list(request, *args, **kwargs)

    def retrieve_by_href(self, request, category_href=None):
        logger.debug(f"retrieve_by_href called with category_href={category_href}")
        try:
            category = Category.objects.get(category_href=category_href)
            serializer = self.get_serializer(category)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            logger.error(f"Category not found for category_href={category_href}")
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Invalid payment data for user {request.user.id}: {serializer.errors}")
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = serializer.validated_data['order']
        amount = serializer.validated_data['amount']

        try:
            with transaction.atomic():
                # Блокуємо замовлення
                order = Order.objects.select_for_update().get(id=order.id)
                if order.status != 'pending':
                    logger.error(f"Invalid order status {order.status} for payment by user {request.user.id}")
                    return Response(
                        {"success": False, "errors": {"order": ["Замовлення не в статусі pending"]}},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if order.total_amount != amount:
                    logger.error(f"Invalid payment amount {amount} for order {order.id} by user {request.user.id}")
                    return Response(
                        {"success": False, "errors": {"amount": ["Сума платежу не відповідає сумі замовлення"]}},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                serializer.save(user=self.request.user)
                logger.info(f"Payment created for order {order.id} by user {request.user.id}")

            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Order.DoesNotExist:
            logger.error(f"Order {order.id} not found for user {request.user.id}")
            return Response(
                {"success": False, "errors": {"order": ["Замовлення не знайдено"]}},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error creating payment for user {request.user.id}: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )

class ShippingViewSet(viewsets.ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user']
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShippingFilter

    def get_queryset(self):
        return Shipping.objects.filter(order__customer=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Invalid shipping data for user {request.user.id}: {serializer.errors}")
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = serializer.validated_data['order']

        try:
            with transaction.atomic():
                # Блокуємо замовлення
                order = Order.objects.select_for_update().get(id=order.id)
                if order.status != 'paid':
                    logger.error(f"Invalid order status {order.status} for shipping by user {request.user.id}")
                    return Response(
                        {"success": False, "errors": {"order": ["Замовлення не оплачено"]}},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                if Shipping.objects.filter(order=order).exists():
                    logger.error(f"Shipping already exists for order {order.id} by user {request.user.id}")
                    return Response(
                        {"success": False, "errors": {"order": ["Доставка вже створена для цього замовлення"]}},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                serializer.save()
                logger.info(f"Shipping created for order {order.id} by user {request.user.id}")

            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Order.DoesNotExist:
            logger.error(f"Order {order.id} not found for user {request.user.id}")
            return Response(
                {"success": False, "errors": {"order": ["Замовлення не знайдено"]}},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error creating shipping for user {request.user.id}: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )

class UserProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response({"success": True, "data": serializer.data})

class HitsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    @extend_schema(
        responses={200: ProductSerializer(many=True)},
        description="Повертає топ-10 продуктів за кількістю відгуків, виключаючи товари типу аукціон."
    )
    def get_queryset(self):
        logger.info("HitsView accessed, returning top 10 products by rating_count, excluding auctions")
        return Product.objects.filter(stock__gt=0, sale_type='fixed', is_approved=True).order_by('-rating_count')[:10]

class PopularCategoriesView(APIView):
    @extend_schema(
        responses={200: CategorySerializer(many=True)},
        description="Тимчасово повертає всі категорії як популярні."
    )
    def get(self, request, *args, **kwargs):
        logger.info("PopularCategoriesView accessed, returning temporary data")
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(
            {
                "success": True,
                "data": serializer.data,
                "message": "Тимчасові дані для популярних категорій (всі категорії)."
            },
            status=status.HTTP_200_OK
        )

class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                logger.error("Refresh token not found in cookies")
                return Response(
                    {"success": False, "errors": {"detail": "Refresh token not found in cookies"}},
                    status=status.HTTP_400_BAD_REQUEST
                )
            logger.info(f"Adding refresh token to blacklist for user {request.user.id}")
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"Refresh token successfully blacklisted")
            response = Response(
                {"success": True, "message": "Logged out successfully"},
                status=status.HTTP_200_OK
            )
            response.delete_cookie(
                key='refresh_token',
                path='/',
                domain=None,
                samesite='None'
            )
            return response
        except TokenError as e:
            logger.error(f"Token error during logout: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )

class PlatformReviewListView(generics.ListAPIView):
    queryset = PlatformReview.objects.all()
    serializer_class = PlatformReviewSerializer

class DiscountedProductsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    @extend_schema(
        responses={200: ProductSerializer(many=True)},
        description="Повертає список товарів зі знижками (discount_price не null)."
    )
    def get_queryset(self):
        logger.info("DiscountedProductsView accessed, returning products with discounts")
        return Product.objects.filter(stock__gt=0, sale_type='fixed', discount_price__isnull=False, is_approved=True)


class SearchViewSet(GenericViewSet):
    permission_classes = []
    pagination_class = StandardResultsSetPagination
    serializer_class = SearchResultSerializer
    throttle_scope = 'search'

    @extend_schema(
        parameters=[
            OpenApiParameter(name='q', description='Search query', required=True, type=str),
            OpenApiParameter(name='similarity_threshold', description='Trigram similarity threshold', required=False, type=float, default=0.3),
        ],
        responses={200: SearchResultSerializer(many=True)},
        examples=[
            OpenApiExample(
                'Example Response',
                value={
                    'success': True,
                    'count': 3,
                    'next': None,
                    'prev': None,
                    'results': [
                        {'type': 'user', 'id': 1, 'name': 'Тест Користувач', 'relevance': 0.9, 'details': {}},
                        {'type': 'product', 'id': 2, 'name': 'Смартфон', 'relevance': 0.8, 'details': {}},
                        {'type': 'category', 'id': 3, 'name': 'Електроніка', 'relevance': 0.7, 'details': {}}
                    ]
                }
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        try:
            similarity_threshold = float(request.GET.get('similarity_threshold', 0.3))
        except (TypeError, ValueError):
            return Response(
                {"success": False, "errors": {"similarity_threshold": "Невірне значення similarity_threshold"}},
                status=status.HTTP_400_BAD_REQUEST)

        if len(query) > 100:
            logger.warning(f"Search query too long: {len(query)} characters")
            return Response({"success": False, "errors": {"query": "Запит занадто довгий (макс. 100 символів)"}},
                            status=status.HTTP_400_BAD_REQUEST)

        if not query:
            logger.warning("Search request with empty query")
            return Response({"success": False, "errors": {"query": "Пошуковий запит не може бути порожнім"}},
                            status=status.HTTP_400_BAD_REQUEST)

        logger.debug(f"Search request with query: {query}, similarity_threshold: {similarity_threshold}")

        try:
            search_query = SearchQuery(query, config='ukrainian')

            user_data = User.objects.annotate(
                rank=SearchRank('search_vector', search_query),
                similarity=TrigramSimilarity('username', query) + TrigramSimilarity('surname', query),
                type=Value('user', output_field=CharField()),
                full_name=Concat('username', Value(' '), 'surname'),
                relevance=SearchRank('search_vector', search_query) + TrigramSimilarity('username', query) + TrigramSimilarity('surname', query)
            ).filter(
                (Q(search_vector=search_query) | Q(similarity__gt=similarity_threshold)) & Q(is_active=True) & Q(is_verified=True)
            ).values('type', 'id', 'full_name', 'relevance')

            product_data = Product.objects.annotate(
                rank=SearchRank('search_vector', search_query),
                similarity=TrigramSimilarity('name', query) + TrigramSimilarity('description', query),
                type=Value('product', output_field=CharField()),
                full_name=F('name'),  # Використовуємо full_name для уніфікації
                relevance=SearchRank('search_vector', search_query) + TrigramSimilarity('name', query) + TrigramSimilarity('description', query)
            ).filter(
                (Q(search_vector=search_query) | Q(similarity__gt=similarity_threshold)) & Q(stock__gt=0)
            ).values('type', 'id', 'full_name', 'relevance')

            category_data = Category.objects.annotate(
                rank=SearchRank('search_vector', search_query),
                similarity=TrigramSimilarity('name', query),
                type=Value('category', output_field=CharField()),
                full_name=F('name'),
                relevance=SearchRank('search_vector', search_query) + TrigramSimilarity('name', query)
            ).filter(
                Q(search_vector=search_query) | Q(similarity__gt=similarity_threshold)
            ).values('type', 'id', 'full_name', 'relevance')

            # Об'єднуємо усі дані (union) — order_by тут не працює
            data = user_data.union(product_data, category_data)

            data_list = list(data)

            # Сортуємо в Python за relevance desc
            data_list.sort(key=lambda x: x['relevance'], reverse=True)

            max_results = 1000
            if len(data_list) > max_results:
                logger.warning(f"Search query '{query}' returned too many results: {len(data_list)}")
                data_list = data_list[:max_results]

            # Переіменовуємо full_name у name для серіалізатора
            for item in data_list:
                item['name'] = item.pop('full_name')

            user_ids = [item['id'] for item in data_list if item['type'] == 'user']
            product_ids = [item['id'] for item in data_list if item['type'] == 'product']
            category_ids = [item['id'] for item in data_list if item['type'] == 'category']

            users = User.objects.filter(id__in=user_ids).select_related()
            products = Product.objects.filter(id__in=product_ids).select_related('vendor', 'category').prefetch_related('images')
            categories = Category.objects.filter(id__in=category_ids).select_related('parent')

            user_dict = {u.id: u for u in users}
            product_dict = {p.id: p for p in products}
            category_dict = {c.id: c for c in categories}

            logger.info(f"Search found {len(user_ids)} users, {len(product_ids)} products, {len(category_ids)} categories for query '{query}'")

            page = self.paginate_queryset(data_list)
            if page is not None:
                serializer = self.get_serializer(page, many=True, context={
                    'user_dict': user_dict,
                    'product_dict': product_dict,
                    'category_dict': category_dict
                })
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(data_list, many=True, context={
                'user_dict': user_dict,
                'product_dict': product_dict,
                'category_dict': category_dict
            })

            logger.info(f"Search completed for query '{query}' with {len(data_list)} results")

            return Response({
                "success": True,
                "count": len(data_list),
                "next": None,
                "prev": None,
                "results": serializer.data
            }, status=status.HTTP_200_OK)

        except DatabaseError as e:
            logger.error(f"Database error during search for query '{query}': {str(e)}")
            return Response({"success": False, "errors": {"detail": "Помилка бази даних"}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError as e:
            logger.error(f"Value error during search for query '{query}': {str(e)}", exc_info=True)
            return Response({"success": False, "errors": {"detail": f"Невірний формат запиту: {str(e)}"}},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during search for query '{query}': {str(e)}")
            return Response({"success": False, "errors": {"detail": str(e)}}, status=status.HTTP_400_BAD_REQUEST)

class ModerationViewSet(viewsets.ViewSet):
    permission_classes = [HasRolePermission]
    allowed_roles = ['admin']
    throttle_scope = 'moderation'

    @extend_schema(
        parameters=[
            OpenApiParameter(name='type', description='Type of content to moderate (product/review)', required=True, type=str),
            OpenApiParameter(name='is_approved', description='Filter by approval status', required=False, type=bool),
        ],
        responses={200: serializers.Serializer},
        description="Retrieve content pending moderation (products or reviews)"
    )
    def list(self, request):
        content_type = request.query_params.get('type')
        is_approved = request.query_params.get('is_approved', None)

        if content_type not in ['product', 'review']:
            logger.error(f"Invalid content type {content_type} for moderation")
            return Response(
                {"success": False, "errors": {"type": "Тип контенту має бути 'product' або 'review'"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if content_type == 'product':
                queryset = Product.objects.all()
                if is_approved is not None:
                    queryset = queryset.filter(is_approved=is_approved.lower() == 'true')
                serializer = ProductSerializer(queryset, many=True)
            else:  # content_type == 'review'
                queryset = Review.objects.all()
                if is_approved is not None:
                    queryset = queryset.filter(is_approved=is_approved.lower() == 'true')
                serializer = ReviewSerializer(queryset, many=True)

            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing moderation content for type {content_type}: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(
        parameters=[
            OpenApiParameter(name='type', description='Type of content (product/review)', required=True, type=str),
            OpenApiParameter(name='id', description='ID of the content to moderate', required=True, type=int),
            OpenApiParameter(name='is_approved', description='Approval status', required=True, type=bool),
        ],
        responses={200: None},
        description="Approve or reject content (product/review)"
    )
    @action(detail=False, methods=['post'])
    def moderate(self, request):
        logger.debug(f"Moderation request by user {request.user.id} with data: {request.data}")
        content_type = request.data.get('type')
        content_id = request.data.get('id')
        is_approved = request.data.get('is_approved')

        if content_type not in ['product', 'review']:
            logger.error(f"Invalid content type {content_type} for moderation")
            return Response(
                {"success": False, "errors": {"type": "Тип контенту має бути 'product' або 'review'"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(is_approved, bool):
            logger.error(f"Invalid is_approved value {is_approved} for moderation")
            return Response(
                {"success": False, "errors": {"is_approved": "is_approved має бути булевим значенням"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                if content_type == 'product':
                    try:
                        content = Product.objects.select_for_update().get(id=content_id)
                    except Product.DoesNotExist:
                        logger.error(f"Product {content_id} not found for moderation")
                        return Response(
                            {"success": False, "errors": {"id": "Продукт не знайдено"}},
                            status=status.HTTP_404_NOT_FOUND
                        )
                else:  # content_type == 'review'
                    try:
                        content = Review.objects.select_for_update().get(id=content_id)
                    except Review.DoesNotExist:
                        logger.error(f"Review {content_id} not found for moderation")
                        return Response(
                            {"success": False, "errors": {"id": "Відгук не знайдено"}},
                            status=status.HTTP_404_NOT_FOUND
                        )

                content.is_approved = is_approved
                content.save()

                # Якщо відгук схвалено або відхилено, оновлюємо rating_count продукту
                if content_type == 'review':
                    product = content.product
                    product.rating_count = product.reviews.filter(is_approved=True).count()
                    product.save(update_fields=['rating_count'])

                logger.info(f"{content_type.capitalize()} {content_id} moderated by user {request.user.id} to is_approved={is_approved}")
                return Response(
                    {"success": True, "message": f"{content_type.capitalize()} {'схвалено' if is_approved else 'відхилено'}"},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            logger.error(f"Error moderating {content_type} {content_id}: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )
