from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, VerifyEmailView, ResendVerificationCodeView, LoginView, CustomTokenRefreshView,
    PasswordResetRequestView, PasswordResetConfirmView, UserViewSet, UserProfileView,
    CategoryViewSet, ProductViewSet, OrderViewSet, CartAddView, CartRemoveView, CartListView,
    ReviewViewSet, AuctionBidViewSet, FavoriteViewSet, PaymentViewSet, ShippingViewSet,
    CategoryImageUploadView, ProductImageUploadView, LogoutView, PlatformReviewListView
)

urlpatterns = [
    # Аутентифікаційні маршрути
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/verify-email/<str:uidb64>/<str:token>/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('auth/resend-verification-code/', ResendVerificationCodeView.as_view(), name='resend-verification-code'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('auth/password-reset-confirm/<str:uidb64>/<str:token>/', views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),

    # Нові маршрути для заглушок
    path('hits/', views.HitsView.as_view({'get': 'list'}), name='hits'),
    path('popular-categories/', views.PopularCategoriesView.as_view(), name='popular-categories'),

    # Інші маршрути
    path('users/', views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('user/', views.UserProfileView.as_view(), name='user-profile'),
    path('users/<int:pk>/', views.UserViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),
    path('categories/', views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
    path('categories/image-upload/', views.CategoryImageUploadView.as_view(), name='category-image-upload'),
    path('categories/<int:pk>/', views.CategoryViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='category-detail'),
    path('discounted-products/', views.DiscountedProductsView.as_view({'get': 'list'}), name='discounted-products'),
    path('products/', views.ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('products/image-upload/', views.ProductImageUploadView.as_view(), name='product-image-upload'),
    path('products/<int:pk>/', views.ProductViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='product-detail'),
    path('orders/', views.OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='order-list'),
    path('orders/<int:pk>/', views.OrderViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='order-detail'),
    path('cart/add/', views.CartAddView.as_view(), name='cart-add'),
    path('cart/remove/', views.CartRemoveView.as_view(), name='cart-remove'),
    path('cart/', views.CartListView.as_view(), name='cart-list'),
    path('reviews/', views.ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='review-detail'),
    path('auction-bids/', views.AuctionBidViewSet.as_view({'get': 'list', 'post': 'create'}), name='auction-bid-list'),
    path('auction-bids/<int:pk>/', views.AuctionBidViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='auction-bid-detail'),
    path('favorites/', views.FavoriteViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorite-list'),
    path('favorites/<int:pk>/', views.FavoriteViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='favorite-detail'),
    path('payments/', views.PaymentViewSet.as_view({'get': 'list', 'post': 'create'}), name='payment-list'),
    path('payments/<int:pk>/', views.PaymentViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='payment-detail'),
    path('shipping/', views.ShippingViewSet.as_view({'get': 'list', 'post': 'create'}), name='shipping-list'),
    path('shipping/<int:pk>/', views.ShippingViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='shipping-detail'),
    path('platform-reviews/', PlatformReviewListView.as_view(), name='platform-review-list'),
    path('<slug:category_href>/', views.CategoryViewSet.as_view({'get': 'retrieve_by_href'}),
         name='category-detail-by-href'),
    path('<slug:category_href>/<slug:product_href>/', views.ProductViewSet.as_view(
        {'get': 'retrieve_by_href', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}),
         name='product-detail-by-href'),
]