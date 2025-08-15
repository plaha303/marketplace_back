from django_filters import rest_framework as filters
from .models import User

class UserFilter(filters.FilterSet):
    roles = filters.CharFilter(method='filter_roles')
    is_verified = filters.BooleanFilter(field_name='is_verified', lookup_expr='exact')
    username = filters.CharFilter(field_name='username', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='exact')
    id = filters.NumberFilter(field_name='id', lookup_expr='exact')

    class Meta:
        model = User
        fields = ['roles', 'is_verified', 'username', 'email', 'id']

    def filter_roles(self, queryset, name, value):
        return queryset.filter(roles__contains=[value])