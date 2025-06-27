from django.contrib import admin
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Category, Product, Cart

class AdminAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    login_form = AdminAuthenticationForm
    list_display = ['id', 'username', 'email', 'surname', 'is_verified', 'is_active']
    search_fields = ['id', 'username', 'email']
    list_filter = ['is_verified', 'is_active', 'email']
from django.contrib import admin
from .models import EmailLog

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('order', 'recipient', 'subject', 'status', 'sent_at')
    list_filter = ('status', 'sent_at')
    search_fields = ('recipient', 'subject')

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)