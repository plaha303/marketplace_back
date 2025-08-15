# order_service/urls.py
from django.urls import path, include

urlpatterns = [
    path('', include('app.urls')),
    path('healthcheck/', HealthCheckView.as_view(), name='healthcheck'),
]