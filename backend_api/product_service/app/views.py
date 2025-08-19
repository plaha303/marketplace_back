#product_service/app/views.py
from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category, Review, AuctionBid, Favorite, ProductImage
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer, AuctionBidSerializer, FavoriteSerializer, ProductImageUploadSerializer
from .permissions import HasRolePermission
from .tasks import process_image, send_moderation_notification, moderate_content
from django.db import transaction, connection
from django.db.utils import OperationalError
from django.utils.text import slugify
import logging
from rest_framework.pagination import PageNumberPagination
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import Q

logger = logging.getLogger(__name__)

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

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_approved=True)
    serializer_class = ProductSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['vendor', 'admin']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category_id', 'sale_type', 'is_approved', 'vendor_id']
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        with transaction.atomic():
            instance = serializer.save(vendor_id=self.request.user.id)
            moderate_content.delay('product', instance.id, instance.name)
            logger.info(f"Product {instance.id} created by user {self.request.user.id}")

    def get_queryset(self):
        if 'admin' not in self.request.user.roles:
            return self.queryset.filter(vendor_id=self.request.user.id)
        return self.queryset

    @action(detail=True, methods=['patch'], url_path='update-rating')
    def update_rating(self, request, pk=None):
        product = self.get_object()
        rating_count = request.data.get('rating_count')
        if rating_count is not None:
            product.rating_count = rating_count
            product.save(update_fields=['rating_count'])
            logger.info(f"Updated rating_count for product {product.id}")
            return Response({"success": True}, status=status.HTTP_200_OK)
        return Response({"error": "rating_count required"}, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['admin']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['parent', 'name']
    pagination_class = StandardResultsSetPagination

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.filter(is_approved=True)
    serializer_class = ReviewSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user', 'admin']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_id', 'user_id', 'is_approved']
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        with transaction.atomic():
            instance = serializer.save(user_id=self.request.user.id)
            moderate_content.delay('review', instance.id, instance.comment)
            logger.info(f"Review {instance.id} created by user {self.request.user.id}")

    def get_queryset(self):
        if 'admin' not in self.request.user.roles:
            return self.queryset.filter(user_id=self.request.user.id)
        return self.queryset

class AuctionBidViewSet(viewsets.ModelViewSet):
    queryset = AuctionBid.objects.all()
    serializer_class = AuctionBidSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user', 'admin']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_id', 'user_id']
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
        logger.info(f"Auction bid created for product {serializer.validated_data['product_id']} by user {self.request.user.id}")

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [HasRolePermission]
    allowed_roles = ['user', 'admin']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id', 'product_id']
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
        logger.info(f"Favorite added for product {serializer.validated_data['product_id']} by user {self.request.user.id}")

class ProductImageUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [HasRolePermission]
    allowed_roles = ['vendor', 'admin']

    def post(self, request):
        serializer = ProductImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            image = serializer.validated_data['image']
            result = process_image.delay(product_id, image.read())
            return Response({"success": True, "task_id": result.id}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ModerationViewSet(viewsets.ViewSet):
    permission_classes = [HasRolePermission]
    allowed_roles = ['admin']

    def create(self, request):
        content_type = request.data.get('type')
        content_id = request.data.get('id')
        is_approved = request.data.get('is_approved')

        if content_type not in ['product', 'review']:
            logger.error(f"Invalid content type {content_type} for moderation")
            return Response(
                {"success": False, "errors": {"type": "Content type must be 'product' or 'review'"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(content_id, int):
            logger.error(f"Invalid content ID {content_id} for moderation")
            return Response(
                {"success": False, "errors": {"id": "Content ID must be an integer"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(is_approved, bool):
            logger.error(f"Invalid is_approved value {is_approved} for moderation")
            return Response(
                {"success": False, "errors": {"is_approved": "is_approved must be a boolean"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                if content_type == 'product':
                    obj = Product.objects.get(id=content_id)
                    recipient_id = obj.vendor_id
                else:  # review
                    obj = Review.objects.get(id=content_id)
                    recipient_id = obj.user_id

                obj.is_approved = is_approved
                obj.save()
                logger.info(f"{content_type.capitalize()} {content_id} {'approved' if is_approved else 'rejected'} by user {request.user.id}")

                try:
                    response = requests.get(f"{settings.USER_SERVICE_URL}/users/{recipient_id}", timeout=5)
                    response.raise_for_status()
                    recipient_email = response.json()['email']
                except requests.RequestException as e:
                    logger.error(f"Failed to fetch email for user {recipient_id}: {str(e)}")
                    return Response({"success": False, "errors": {"detail": "Failed to fetch user email"}},
                                  status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                send_moderation_notification.delay(content_type, content_id, is_approved, recipient_email)
                return Response(
                    {"success": True, "message": f"{content_type.capitalize()} {'approved' if is_approved else 'rejected'}"},
                    status=status.HTTP_200_OK
                )
        except (Product.DoesNotExist, Review.DoesNotExist):
            logger.error(f"{content_type.capitalize()} with ID {content_id} not found")
            return Response(
                {"success": False, "errors": {"detail": f"{content_type.capitalize()} not found"}},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error moderating {content_type} {content_id}: {str(e)}")
            return Response(
                {"success": False, "errors": {"detail": str(e)}},
                status=status.HTTP_400_BAD_REQUEST
            )

class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return Response({"status": "healthy", "database": "ok"}, status=status.HTTP_200_OK)
        except OperationalError:
            return Response({"status": "unhealthy", "database": "failed"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
