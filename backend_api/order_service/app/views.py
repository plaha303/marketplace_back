# order_service/app/views.py
from django.db import connection
from django.db.utils import OperationalError
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .tasks import send_order_status_update_email
from .serializers import OrderSerializer
from .permissions import HasRolePermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
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



class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return Response({"status": "healthy", "database": "ok"}, status=status.HTTP_200_OK)
        except OperationalError:
            return Response({"status": "unhealthy", "database": "failed"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

