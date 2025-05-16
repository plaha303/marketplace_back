import logging
from typing import List
from rest_framework import permissions
from django.db import DatabaseError

logger = logging.getLogger(__name__)

class HasGroupPermission(permissions.BasePermission):
    """
    Перевіряє права доступу на основі груп.
    - GET: дозволено всім (авторизованим і неавторизованим).
    - POST: дозволено групам, указаним у allowed_groups.
    - PUT/PATCH/DELETE: залежить від груп і власника об'єкта.
    """
    ADMIN_GROUP_NAME = 'Admins'

    def has_permission(self, request, view):
        """
        Перевіряє, чи має користувач дозвіл для виконання запиту.

        Args:
            request: HTTP-запит.
            view: Вью, для якого перевіряються дозволи.

        Returns:
            bool: True, якщо доступ дозволено, інакше False.
        """
        # Дозволяємо GET-запити для всіх
        if request.method in permissions.SAFE_METHODS:
            return True

        # Для інших методів потрібна автентифікація
        if not request.user.is_authenticated:
            return False

        # Перевіряємо дозволені групи
        allowed_groups: List[str] = getattr(view, 'allowed_groups', [])
        if not allowed_groups and request.method not in permissions.SAFE_METHODS:
            logger.warning(f"No allowed_groups defined for view {view.__class__.__name__} ({request.method})")
            return False

        try:
            logger.debug(f"Checking groups {allowed_groups} for user {request.user.id}")
            return request.user.groups.filter(name__in=allowed_groups).exists()
        except DatabaseError as e:
            logger.error(f"Database error in {view.__class__.__name__} for user {request.user.id}: {e}")
            return False
        except Exception as e:
            logger.critical(f"Unexpected error in {view.__class__.__name__} for user {request.user.id}: {e}")
            return False

    def has_object_permission(self, request, view, obj):
        """
        Перевіряє, чи має користувач дозвіл для роботи з конкретним об'єктом.

        Args:
            request: HTTP-запит.
            view: Вью, для якого перевіряються дозволи.
            obj: Об'єкт, до якого застосовується перевірка.

        Returns:
            bool: True, якщо доступ дозволено, інакше False.
        """
        # Дозволяємо GET-запити для всіх
        if request.method in permissions.SAFE_METHODS:
            return True

        # Перевіряємо дозволені групи
        allowed_groups: List[str] = getattr(view, 'allowed_groups', [])
        if not allowed_groups and request.method not in permissions.SAFE_METHODS:
            logger.warning(f"No allowed_groups defined for view {view.__class__.__name__} ({request.method})")
            return False

        try:
            user_groups = set(request.user.groups.values_list('name', flat=True))
            has_group = any(group in allowed_groups for group in user_groups)
            if not has_group:
                return False

            # Admins можуть усе
            if self.ADMIN_GROUP_NAME in user_groups:
                return True

            # Vendors можуть редагувати/видаляти лише свої продукти
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                vendor = getattr(obj, 'vendor', None)
                if vendor is not None:
                    return vendor == request.user
                return False  # Якщо vendor відсутній, забороняємо доступ (залежить від вимог)

            # Для інших випадків достатньо належності до групи
            return has_group
        except DatabaseError as e:
            logger.error(f"Database error in {view.__class__.__name__} for user {request.user.id}, object {obj.__class__.__name__}: {e}")
            return False
        except Exception as e:
            logger.critical(f"Unexpected error in {view.__class__.__name__} for user {request.user.id}, object {obj.__class__.__name__}: {e}")
            return False