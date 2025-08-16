# order_service/app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, HealthCheckView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('healthcheck/', HealthCheckView.as_view(), name='healthcheck'),
    path('orders/info/', OrderInfoView.as_view(), name='order_info'),
]