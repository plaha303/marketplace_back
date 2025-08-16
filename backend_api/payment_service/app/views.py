from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
from .permissions import HasRolePermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
import logging

logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user', 'admin']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order_id', 'status', 'created_at']
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save()
        logger.info(f"Payment created for order {serializer.validated_data['order_id']}")

    def get_queryset(self):
        if 'admin' not in self.request.user.roles:
            return self.queryset.filter(order_id__in=Order.objects.filter(customer_id=self.request.user.id).values('id'))
        return self.queryset

class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return Response({"status": "healthy", "database": "ok"}, status=status.HTTP_200_OK)
        except OperationalError:
            return Response({"status": "unhealthy", "database": "failed"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

