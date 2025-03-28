from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (UserViewSet, ProductViewSet, OrderViewSet, RegisterView, VerifyEmailView, 
                    LoginView, PasswordResetRequestView, PasswordResetConfirmView, 
                    CartAddView, CartRemoveView, CartListView)

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='order-list'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('auth/password-reset-confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('cart/add/', CartAddView.as_view(), name='cart-add'),
    path('cart/remove/', CartRemoveView.as_view(), name='cart-remove'),
    path('cart/', CartListView.as_view(), name='cart-list'),
]
