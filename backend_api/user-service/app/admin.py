import logging
from django.contrib import admin
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmailLog

logger = logging.getLogger(__name__)

class AdminAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)

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

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'recipient', 'subject', 'status', 'sent_at']
    list_filter = ['status', 'sent_at']
    search_fields = ['recipient', 'subject', 'error']
    fields = ['order', 'recipient', 'subject', 'status', 'error', 'sent_at']
    readonly_fields = ['sent_at', 'error']