from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import HealthCheckView, OrderInfoView
urlpatterns = [
    path('orders/info/', OrderInfoView.as_view(), name='order_info'),
    path('healthcheck/', HealthCheckView.as_view(), name='healthcheck'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/verify-email/<str:uidb64>/<str:token>/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('auth/resend-verification-code/', views.ResendVerificationCodeView.as_view(), name='resend-verification-code'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('auth/password-reset-confirm/<str:uidb64>/<str:token>/', views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('users/', views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('user/', views.UserProfileView.as_view(), name='user-profile'),
    path('users/<int:pk>/', views.UserViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),
]