from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, HealthCheckView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('healthcheck/', HealthCheckView.as_view(), name='healthcheck'),
]