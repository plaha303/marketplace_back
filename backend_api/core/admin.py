import logging
from django.contrib import admin
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Category, Product, ProductImage, Cart, EmailLog, AuctionBid,
    Order, OrderItem, Payment, Shipping, Review, Favorite, PlatformReview
)

logger = logging.getLogger(__name__)

# Форма для аутентифікації адміна
class AdminAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)

# Форма для редагування користувача в адмінці
class UserAdminForm(forms.ModelForm):
    roles = forms.CharField(
        label="Ролі",
        widget=forms.TextInput(attrs={'placeholder': 'Введіть ролі через кому, наприклад: admin,user'}),
        required=False,
        help_text="Введіть ролі через кому (наприклад, admin,user)."
    )

    class Meta:
        model = User
        fields = '__all__'

    def clean_roles(self):
        roles_input = self.cleaned_data.get('roles')
        if roles_input:
            roles = [role.strip() for role in roles_input.split(',') if role.strip()]
            valid_roles = [choice[0] for choice in User.ROLE_CHOICES]
            if not all(role in valid_roles for role in roles):
                raise forms.ValidationError(f"Ролі повинні бути з: {valid_roles}")
            return roles
        return []

# Форма для створення суперкористувача
class SuperUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Паролі не збігаються.")
        return password2

    def save(self, commit=True):
        logger.debug("Початок створення суперкористувача з email: %s", self.cleaned_data.get('email'))
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_verified = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.roles = ['admin']
        logger.debug("Перед збереженням: is_verified=%s, roles=%s", user.is_verified, user.roles)
        if commit:
            user.save()
            logger.debug("Після першого збереження: is_verified=%s, roles=%s", user.is_verified, user.roles)
            # Додаткове збереження для забезпечення правильних значень
            user.is_verified = True
            user.roles = ['admin']
            user.save()
            logger.debug("Після другого збереження: is_verified=%s, roles=%s", user.is_verified, user.roles)
        return user

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserAdminForm
    add_form = SuperUserCreationForm
    login_form = AdminAuthenticationForm
    list_display = ['id', 'username', 'email', 'surname', 'roles', 'is_verified', 'is_active']
    search_fields = ['id', 'username', 'email', 'surname']
    list_filter = ['is_verified', 'is_active', 'roles']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'surname', 'password')}),
        ('Ролі та статус', {'fields': ('roles', 'is_verified', 'is_active', 'is_staff', 'is_superuser')}),
        ('Додаткова інформація', {'fields': ('verification_token_created_at',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ['verification_token_created_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and 'admin' not in request.user.roles:
            logger.warning(f"User {request.user.id} attempted to access User list without admin role")
            qs = qs.filter(id=request.user.id)
        return qs

# Інлайн для ProductImage
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image_url']

# Інлайн для OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity', 'price']
    readonly_fields = ['price']

# Інлайн для AuctionBid
class AuctionBidInline(admin.TabularInline):
    model = AuctionBid
    extra = 0
    fields = ['user', 'amount', 'created_at']
    readonly_fields = ['user', 'amount', 'created_at']

# Інлайн для Review
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ['user', 'rating', 'comment', 'created_at']
    readonly_fields = ['user', 'rating', 'comment', 'created_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent_name', 'category_href']
    list_filter = ['parent']
    search_fields = ['name', 'category_href']
    prepopulated_fields = {'category_href': ('name',)}
    fields = ['name', 'parent', 'category_image', 'category_href']

    def parent_name(self, obj):
        return obj.parent.name if obj.parent else '---'
    parent_name.short_description = 'Батьківська категорія'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['parent'].required = False
        if obj:
            form.base_fields['parent'].queryset = Category.objects.exclude(id=obj.id)
        return form

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'vendor', 'category', 'sale_type', 'price', 'stock', 'is_available', 'created_at']
    list_filter = ['sale_type', 'category', 'vendor']
    search_fields = ['name', 'product_href', 'description']
    prepopulated_fields = {'product_href': ('name',)}
    fields = [
        'name', 'vendor', 'category', 'description', 'sale_type',
        'price', 'start_price', 'auction_end_time', 'stock', 'product_href'
    ]
    inlines = [ProductImageInline, AuctionBidInline, ReviewInline]
    list_select_related = ['vendor', 'category']

    def is_available(self, obj):
        return obj.is_available()
    is_available.boolean = True
    is_available.short_description = 'В наявності'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and 'admin' not in request.user.roles:
            qs = qs.filter(vendor=request.user)
        return qs

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    list_filter = ['user']
    search_fields = ['user__username', 'product__name']
    fields = ['user', 'product', 'quantity']
    readonly_fields = ['user', 'product']

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'recipient', 'subject', 'status', 'sent_at']
    list_filter = ['status', 'sent_at']
    search_fields = ['recipient', 'subject', 'error']
    fields = ['order', 'recipient', 'subject', 'status', 'error', 'sent_at']
    readonly_fields = ['sent_at', 'error']

@admin.register(PlatformReview)
class PlatformReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'city', 'rating', 'created_at']
    search_fields = ['name', 'surname', 'city', 'review_text']
    list_filter = ['rating', 'created_at']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'image_url']
    list_filter = ['product']
    search_fields = ['product__name', 'image_url']
    fields = ['product', 'image_url']

@admin.register(AuctionBid)
class AuctionBidAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'amount', 'created_at']
    list_filter = ['product', 'user']
    search_fields = ['product__name', 'user__username']
    fields = ['product', 'user', 'amount', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'customer']
    search_fields = ['customer__username', 'customer__email']
    fields = ['customer', 'total_amount', 'status', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    list_select_related = ['customer']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and 'admin' not in request.user.roles:
            qs = qs.filter(customer=request.user)
        return qs

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
    list_filter = ['order', 'product']
    search_fields = ['order__id', 'product__name']
    fields = ['order', 'product', 'quantity', 'price']
    readonly_fields = ['price']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'user', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['order__id', 'user__username']
    fields = ['order', 'user', 'amount', 'payment_method', 'status', 'created_at']
    readonly_fields = ['created_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and 'admin' not in request.user.roles:
            qs = qs.filter(user=request.user)
        return qs

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'recipient_name', 'city', 'country', 'shipped_at']
    list_filter = ['city', 'country', 'shipped_at']
    search_fields = ['recipient_name', 'address', 'tracking_number']
    fields = [
        'order', 'recipient_name', 'address', 'city',
        'postal_code', 'country', 'tracking_number', 'shipped_at'
    ]
    readonly_fields = ['shipped_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and 'admin' not in request.user.roles:
            qs = qs.filter(order__customer=request.user)
        return qs

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'product']
    search_fields = ['product__name', 'user__username', 'comment']
    fields = ['product', 'user', 'rating', 'comment', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']
    list_filter = ['user', 'product']
    search_fields = ['user__username', 'product__name']
    fields = ['user', 'product']
    readonly_fields = ['user', 'product']