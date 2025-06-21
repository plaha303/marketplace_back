from django.contrib import admin
from django import forms
from .models import User, Category, Product, Cart

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'surname', 'is_verified', 'is_active']
    search_fields = ['id', 'username', 'email']
    list_filter = ['is_verified', 'is_active', 'email']  # Додано фільтр за email

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)