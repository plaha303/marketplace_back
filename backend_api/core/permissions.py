import logging
from typing import List
from rest_framework import permissions
from django.db import DatabaseError

logger = logging.getLogger(__name__)

class HasRolePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            logger.debug(f"Allowing SAFE method {request.method} for view {view.__class__.__name__}")
            return True

        if not request.user.is_authenticated:
            logger.debug(f"User not authenticated for {request.method} in {view.__class__.__name__}")
            return False

        allowed_roles: List[str] = getattr(view, 'allowed_roles', [])
        if not allowed_roles and request.method not in permissions.SAFE_METHODS:
            logger.warning(f"No allowed_roles defined for view {view.__class__.__name__} ({request.method})")
            return False

        try:
            user_roles = request.user.roles or []
            logger.debug(f"Checking roles {allowed_roles} against user roles {user_roles} for user {request.user.id}")
            has_role = any(role in user_roles for role in allowed_roles)
            if not has_role:
                logger.warning(f"User {request.user.id} lacks required roles {allowed_roles}")
            return has_role
        except DatabaseError as e:
            logger.error(f"Database error in {view.__class__.__name__} for user {request.user.id}: {e}")
            return False
        except Exception as e:
            logger.critical(f"Unexpected error in {view.__class__.__name__} for user {request.user.id}: {e}")
            return False

    def has_object_permission(self, request, view, obj):
        logger.debug(f"Checking object permission for {request.method} in {view.__class__.__name__}")
        if request.method in permissions.SAFE_METHODS:
            logger.debug(f"Allowing SAFE method {request.method} for object {obj.__class__.__name__}")
            return True

        if request.method == 'POST':
            logger.debug(f"Skipping object permission check for POST in {view.__class__.__name__}")
            return True

        allowed_roles: List[str] = getattr(view, 'allowed_roles', [])
        if not allowed_roles:
            logger.warning(f"No allowed_roles defined for view {view.__class__.__name__} ({request.method})")
            return False

        try:
            user_roles = request.user.roles or []
            logger.debug(f"Checking object permission for user {request.user.id} with roles {user_roles}")
            if not any(role in user_roles for role in allowed_roles):
                logger.warning(f"User {request.user.id} lacks required roles {allowed_roles}")
                return False

            if 'admin' in user_roles:
                logger.debug(f"User {request.user.id} is admin, allowing access")
                return True

            vendor = getattr(obj, 'vendor', None)
            customer = getattr(obj, 'customer', None)
            user = getattr(obj, 'user', None)
            if vendor is not None:
                result = vendor == request.user
                logger.debug(f"Vendor check: {result} for user {request.user.id}")
                return result
            elif customer is not None:
                result = customer == request.user
                logger.debug(f"Customer check: {result} for user {request.user.id}")
                return result
            elif user is not None:
                result = user == request.user
                logger.debug(f"User check: {result} for user {request.user.id}")
                return result
            logger.warning(f"No ownership fields found for object {obj.__class__.__name__}")
            return False
        except DatabaseError as e:
            logger.error(f"Database error in {view.__class__.__name__} for user {request.user.id}, object {obj.__class__.__name__}: {e}")
            return False
        except Exception as e:
            logger.critical(f"Unexpected error in {view.__class__.__name__} for user {request.user.id}, object {obj.__class__.__name__}: {e}")
            return False
class ReviewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            logger.debug(f"Allowing SAFE method {request.method} for view {view.__class__.__name__}")
            return True
        if not request.user.is_authenticated:
            logger.debug(f"User not authenticated for {request.method} in {view.__class__.__name__}")
            return False
        allowed_roles = getattr(view, 'allowed_roles', [])
        user_roles = request.user.roles or []
        logger.debug(f"Checking roles {allowed_roles} against user roles {user_roles} for user {request.user.id}")
        return any(role in user_roles for role in allowed_roles)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            logger.debug(f"Allowing SAFE method {request.method} for object {obj.__class__.__name__}")
            return True
        allowed_roles = getattr(view, 'allowed_roles', [])
        user_roles = request.user.roles or []
        if not any(role in user_roles for role in allowed_roles):
            logger.warning(f"User {request.user.id} lacks required roles {allowed_roles}")
            return False
        if 'admin' in user_roles:
            return True
        return obj.user == request.user