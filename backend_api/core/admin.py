from django.contrib import admin
from django import forms
from .models import User, Category, Product, Cart

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ['username', 'email', 'is_verified', 'is_active']
    list_filter = ['is_verified', 'is_active']
    search_fields = ['username', 'email']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'surname', 'roles', 'is_verified', 'is_active')}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)