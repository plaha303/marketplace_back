import logging
from typing import List
from rest_framework import permissions

logger = logging.getLogger(__name__)

class HasRolePermission(permissions.BasePermission):
    """
    Перевіряє права доступу на основі ролей.
    - GET: дозволено всім (авторизованим і неавторизованим).
    - POST: дозволено ролям, указаним у allowed_roles.
    - PUT/PATCH/DELETE: залежить від ролей і власника об'єкта.
    """
    ADMIN_ROLE = 'admin'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        allowed_roles: List[str] = getattr(view, 'allowed_roles', [])
        if not allowed_roles and request.method not in permissions.SAFE_METHODS:
            logger.warning(f"No allowed_roles defined for view {view.__class__.__name__} ({request.method})")
            return False

        try:
            user_roles = request.user.get_roles() if hasattr(request.user, 'get_roles') else request.user.roles
            logger.debug(f"Checking roles {allowed_roles} for user {request.user.id}")
            return any(role in allowed_roles for role in user_roles)
        except Exception as e:
            logger.critical(f"Unexpected error in {view.__class__.__name__} for user {request.user.id}: {e}")
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        allowed_roles: List[str] = getattr(view, 'allowed_roles', [])
        if not allowed_roles and request.method not in permissions.SAFE_METHODS:
            logger.warning(f"No allowed_roles defined for view {view.__class__.__name__} ({request.method})")
            return False

        try:
            user_roles = request.user.get_roles() if hasattr(request.user, 'get_roles') else request.user.roles
            has_role = any(role in allowed_roles for role in user_roles)
            if not has_role:
                return False

            if self.ADMIN_ROLE in user_roles:
                return True

            if request.method in ['PUT', 'PATCH', 'DELETE']:
                vendor = getattr(obj, 'vendor', None)
                if vendor is not None and 'user' in user_roles:
                    return vendor == request.user
                return False

            return has_role
        except Exception as e:
            logger.critical(f"Unexpected error in {view.__class__.__name__} for user {request.user.id}, object {obj.__class__.__name__}: {e}")
            return False