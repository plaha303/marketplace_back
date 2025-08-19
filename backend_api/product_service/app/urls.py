from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, ReviewViewSet, AuctionBidViewSet, FavoriteViewSet, ProductImageUploadView, ModerationViewSet, HealthCheckView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'auction-bids', AuctionBidViewSet, basename='auction-bid')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('healthcheck/', HealthCheckView.as_view(), name='healthcheck'),
    path('', include(router.urls)),
    path('products/image-upload/', ProductImageUploadView.as_view(), name='product-image-upload'),
    path('content/moderation/', ModerationViewSet.as_view({'get': 'list', 'post': 'create'}), name='moderation'),
]