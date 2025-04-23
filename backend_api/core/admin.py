from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group, Permission
from .models import User, Category, Product, Cart

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        groups = cleaned_data.get('groups')
        expected_group = User.ROLE_GROUP_MAPPING.get(role)

        if role == 'admin':
            admin_group = Group.objects.filter(name='Admins').first()
            if not admin_group:
                self.add_error('groups', 'Група Admins не існує. Створіть її перед призначенням ролі admin.')
            elif not groups or admin_group not in groups or len(groups) > 1:
                self.add_error('groups', 'Для ролі admin дозволена лише група Admins.')
        else:
            if expected_group:
                group = Group.objects.filter(name=expected_group).first()
                if group and group not in groups:
                    self.add_error('groups', f"Для ролі {role} потрібно включити групу {expected_group}.")
            if groups and groups.filter(name='Admins').exists():
                self.add_error('groups', 'Група Admins не дозволена для ролі customer, vendor або інших')

        return cleaned_data

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ['username', 'email', 'role', 'is_verified', 'is_active']
    list_filter = ['role', 'is_verified', 'is_active']
    search_fields = ['username', 'email']
    filter_horizontal = ['groups', 'user_permissions']

# Реєстрація моделей
admin.site.register(User, UserAdmin)  # Правильна реєстрація: модель User із класом UserAdmin
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)