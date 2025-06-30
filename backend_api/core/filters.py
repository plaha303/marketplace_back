from django_filters import rest_framework as filters
from .models import Product, Order, User, Cart, Review, AuctionBid, Favorite, Category, Payment, Shipping
from django.utils.timezone import now


class ProductFilter(filters.FilterSet):
    categoryId = filters.NumberFilter(field_name='category__id', lookup_expr='exact')
    sale_type = filters.ChoiceFilter(choices=Product.SALE_TYPE_CHOICES)
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    vendorId = filters.NumberFilter(field_name='vendor__id', lookup_expr='exact')
    in_stock = filters.BooleanFilter(method='filter_in_stock')
    isAvailable = filters.BooleanFilter(method='filter_in_stock')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    is_active_auction = filters.BooleanFilter(method='filter_active_auction')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    stock_min = filters.NumberFilter(field_name='stock', lookup_expr='gte')
    min_rating_count = filters.NumberFilter(method='filter_min_rating_count')
    has_discount = filters.BooleanFilter(method='filter_has_discount')

    class Meta:
        model = Product
        fields = ['categoryId', 'sale_type', 'min_price', 'max_price', 'vendorId', 'in_stock', 'name', 'is_active_auction',
                  'created_after', 'stock_min', 'min_rating_count', 'has_discount']

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        else:
            return queryset.filter(stock__lte=0)

    def filter_active_auction(self, queryset, name, value):
        if value:
            return queryset.filter(sale_type='auction', auction_end_time__gte=now())
        else:
            return queryset.filter(sale_type='auction', auction_end_time__lt=now())

    def filter_min_rating_count(self, queryset, name, value):
        return queryset.filter(rating_count__gte=value)

    def filter_has_discount(self, queryset, name, value):
        if value:
            return queryset.filter(discount_price__isnull=False)
        return queryset


class OrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Order.STATUS_CHOICES)
    min_amount = filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    product = filters.NumberFilter(field_name='items__product__id', lookup_expr='exact')
    customer = filters.NumberFilter(field_name='customer__id', lookup_expr='exact')
    payment_status = filters.ChoiceFilter(field_name='payments__status', choices=Payment.STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ['status', 'min_amount', 'max_amount', 'created_after', 'created_before', 'product', 'customer',
                  'payment_status']


class UserFilter(filters.FilterSet):
    roles = filters.CharFilter(method='filter_roles')
    is_verified = filters.BooleanFilter(field_name='is_verified', lookup_expr='exact')
    username = filters.CharFilter(field_name='username', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='exact')  # Додано
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')  # Додано

    class Meta:
        model = User
        fields = ['roles', 'is_verified', 'username', 'email', 'id']

    def filter_roles(self, queryset, name, value):
        return queryset.filter(roles__contains=[value])


class CartFilter(filters.FilterSet):
    productId = filters.NumberFilter(field_name='product__id', lookup_expr='exact')
    min_quantity = filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    max_quantity = filters.NumberFilter(field_name='quantity', lookup_expr='lte')
    class Meta:
        model = Cart
        fields = ['productId', 'min_quantity', 'max_quantity']


class ReviewFilter(filters.FilterSet):
    product = filters.NumberFilter(field_name='product__id', lookup_expr='exact')
    rating = filters.NumberFilter(field_name='rating', lookup_expr='exact')
    min_rating = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    user = filters.NumberFilter(field_name='user__id', lookup_expr='exact')

    class Meta:
        model = Review
        fields = ['product', 'rating', 'min_rating', 'created_after', 'user']


class AuctionBidFilter(filters.FilterSet):
    product = filters.NumberFilter(field_name='product__id', lookup_expr='exact')
    min_amount = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name='amount', lookup_expr='lte')
    user = filters.NumberFilter(field_name='user__id', lookup_expr='exact')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')

    class Meta:
        model = AuctionBid
        fields = ['product', 'min_amount', 'max_amount', 'user', 'created_after']


class FavoriteFilter(filters.FilterSet):
    product = filters.NumberFilter(field_name='product__id', lookup_expr='exact')
    product_name = filters.CharFilter(field_name='product__name', lookup_expr='icontains')

    class Meta:
        model = Favorite
        fields = ['product', 'product_name']


class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    parent = filters.NumberFilter(field_name='parent__id', lookup_expr='exact')

    class Meta:
        model = Category
        fields = ['name', 'parent']


class PaymentFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Payment.STATUS_CHOICES)
    payment_method = filters.ChoiceFilter(choices=Payment.PAYMENT_METHODS)
    min_amount = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')

    class Meta:
        model = Payment
        fields = ['status', 'payment_method', 'min_amount', 'created_after']


class ShippingFilter(filters.FilterSet):
    city = filters.CharFilter(field_name='city', lookup_expr='icontains')
    country = filters.CharFilter(field_name='country', lookup_expr='exact')
    shipped_after = filters.DateTimeFilter(field_name='shipped_at', lookup_expr='gte')
    tracking_number = filters.CharFilter(field_name='tracking_number', lookup_expr='exact')

    class Meta:
        model = Shipping
        fields = ['city', 'country', 'shipped_after', 'tracking_number']