from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CartListView


urlpatterns = [
    path('users/', views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('user/', views.UserProfileView.as_view(), name='user-profile'),
    path('users/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='user-detail'),
    path('products/', views.ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('products/<int:pk>/', views.ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-detail'),
    path('orders/', views.OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='order-list'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('auth/password-reset-confirm/<str:uidb64>/<str:token>/', views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('cart/add/', views.CartAddView.as_view(), name='cart-add'),
    path('cart/remove/', views.CartRemoveView.as_view(), name='cart-remove'),
    path('cart/', CartListView.as_view(), name='cart-list'),
    path('reviews/', views.ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='review-list'),
    path('auction-bids/', views.AuctionBidViewSet.as_view({'get': 'list', 'post': 'create'}), name='auction-bid-list'),
    path('favorites/', views.FavoriteViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorite-list'),
    path('categories/', views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    path('payments/', views.PaymentViewSet.as_view({'get': 'list', 'post': 'create'}), name='payment-list'),
    path('shipping/', views.ShippingViewSet.as_view({'get': 'list', 'post': 'create'}), name='shipping-list'),
]
