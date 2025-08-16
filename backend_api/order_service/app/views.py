# order_service/app/views.py
from django.db import connection
from django.db.utils import OperationalError
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Order, OrderItem, Cart, CartItem
from .tasks import send_order_status_update_email
from .serializers import OrderSerializer, CartSerializer, CartItemSerializer
from .permissions import HasRolePermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user', 'admin']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'customer_id', 'created_at']
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(customer_id=self.request.user.id)
        logger.info(f"Order created by user {self.request.user.id}")

    def get_queryset(self):
        if 'admin' not in self.request.user.roles:
            return self.queryset.filter(customer_id=self.request.user.id)
        return self.queryset

    def perform_update(self, serializer):
        old_status = self.get_object().status
        instance = serializer.save()
        if old_status != instance.status:
            send_order_status_update_email.delay(instance.id, instance.status)
            logger.info(f"Triggered email for order {instance.id} status change to {instance.status}")

    @action(detail=False, methods=['post'], url_path='from-cart')
    def create_from_cart(self, request):
        try:
            cart = Cart.objects.get(customer_id=request.user.id)
            if not cart.items.exists():
                logger.error(f"Cart for user {request.user.id} is empty")
                return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

            total_amount = sum(item.price * item.quantity for item in cart.items.all())
            order = Order.objects.create(customer_id=request.user.id, total_amount=total_amount, status='pending')

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=item.price
                )

            # Виклик payment_service
            payment_data = {'order_id': order.id, 'amount': order.total_amount, 'status': 'pending'}
            response = requests.post(f"{settings.PAYMENT_SERVICE_URL}/payments/", json=payment_data, timeout=5)
            response.raise_for_status()

            # Виклик shipping_service
            shipping_data = {'order_id': order.id, 'address': request.data.get('address'), 'status': 'pending'}
            response = requests.post(f"{settings.SHIPPING_SERVICE_URL}/shipping/", json=shipping_data, timeout=5)
            response.raise_for_status()

            # Очистити кошик
            cart.items.all().delete()
            logger.info(f"Order {order.id} created from cart for user {request.user.id}")

            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Cart.DoesNotExist:
            logger.error(f"Cart not found for user {request.user.id}")
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except requests.RequestException as e:
            logger.error(f"Failed to create payment/shipping for order: {str(e)}")
            return Response({"error": "Failed to process payment or shipping"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user', 'admin']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer_id']
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(customer_id=self.request.user.id)
        logger.info(f"Cart created by user {self.request.user.id}")

    def get_queryset(self):
        if 'admin' not in self.request.user.roles:
            return self.queryset.filter(customer_id=self.request.user.id)
        return self.queryset

    @action(detail=True, methods=['post'], url_path='add')
    def add_item(self, request, pk=None):
        cart = self.get_object()
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart=cart)
            logger.info(f"Item added to cart {cart.id} by user {request.user.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Failed to add item to cart {cart.id}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='remove')
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        item_id = request.data.get('item_id')
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            item.delete()
            logger.info(f"Item {item_id} removed from cart {cart.id} by user {request.user.id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            logger.error(f"Item {item_id} not found in cart {cart.id}")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='clear')
    def clear_cart(self, request, pk=None):
        cart = self.get_object()
        cart.items.all().delete()
        logger.info(f"Cart {cart.id} cleared by user {request.user.id}")
        return Response(status=status.HTTP_204_NO_CONTENT)


class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return Response({"status": "healthy", "database": "ok"}, status=status.HTTP_200_OK)
        except OperationalError:
            return Response({"status": "unhealthy", "database": "failed"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)