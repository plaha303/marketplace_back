import logging
from typing import List
from rest_framework import permissions
from django.db import DatabaseError

logger = logging.getLogger(__name__)

class HasRolePermission(permissions.BasePermission):
    """
    Перевіряє права доступу на основі ролей.
    - GET: дозволено всім (авторизованим і неавторизованим).
    - POST: дозволено ролям, указаним у allowed_roles.
    - PUT/PATCH/DELETE: залежить від ролей і власника об'єкта.
    """
    def has_permission(self, request, view):
        """
        Перевіряє, чи має користувач дозвіл для виконання запиту.

        Args:
            request: HTTP-запит.
            view: Вью, для якого перевіряються дозволи.

        Returns:
            bool: True, якщо доступ дозволено, інакше False.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        allowed_roles: List[str] = getattr(view, 'allowed_roles', [])
        if not allowed_roles and request.method not in permissions.SAFE_METHODS:
            logger.warning(f"No allowed_roles defined for view {view.__class__.__name__} ({request.method})")
            return False

        try:
            logger.debug(f"Checking roles {allowed_roles} for user {request.user.id}")
            return any(role in request.user.roles for role in allowed_roles)
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
        if request.method in permissions.SAFE_METHODS:
            return True

        allowed_roles: List[str] = getattr(view, 'allowed_roles', [])
        if not allowed_roles and request.method not in permissions.SAFE_METHODS:
            logger.warning(f"No allowed_roles defined for view {view.__class__.__name__} ({request.method})")
            return False

        try:
            if not any(role in request.user.roles for role in allowed_roles):
                return False

            if 'admin' in request.user.roles:
                return True

            if request.method in ['PUT', 'PATCH', 'DELETE']:
                vendor = getattr(obj, 'vendor', None)
                customer = getattr(obj, 'customer', None)
                user = getattr(obj, 'user', None)
                if vendor is not None:
                    return vendor == request.user
                elif customer is not None:
                    return customer == request.user
                elif user is not None:
                    return user == request.user
                return False

            return True
        except DatabaseError as e:
            logger.error(f"Database error in {view.__class__.__name__} for user {request.user.id}, object {obj.__class__.__name__}: {e}")
            return False
        except Exception as e:
            logger.critical(f"Unexpected error in {view.__class__.__name__} for user {request.user.id}, object {obj.__class__.__name__}: {e}")
            return False