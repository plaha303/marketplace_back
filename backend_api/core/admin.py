from django.contrib import admin
from django import forms
from .models import User, Category, Product, Cart

class UserAdminForm(forms.ModelForm):
    roles = forms.MultipleChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select roles for the user (user or admin)."
    )

    class Meta:
        model = User
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        roles = cleaned_data.get('roles', [])
        if not roles:
            self.add_error('roles', 'At least one role must be selected.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.roles = self.cleaned_data['roles']
        if commit:
            user.save()
        return user

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ['username', 'email', 'get_roles_display', 'is_verified', 'is_active']
    list_filter = ['is_verified', 'is_active']
    search_fields = ['username', 'email']
    fields = ['username', 'email', 'roles', 'is_verified', 'is_active', 'is_superuser', 'password']

    def get_roles_display(self, obj):
        return ", ".join(obj.roles)
    get_roles_display.short_description = 'Roles'

# Register models
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)