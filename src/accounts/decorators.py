from functools import wraps
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response

def require_permission(permission_url=None):
    """
    Decorator to check if user has permission for a specific URL
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Get the permission URL from decorator or use the request path
            url_to_check = permission_url or request.path
            
            # Check if user has role and permission
            if not hasattr(request, 'user') or not request.user.is_authenticated:
                return JsonResponse(
                    {'error': 'Authentication required'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Superuser bypass all permissions
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check if user has a role
            if not request.user.role:
                return JsonResponse(
                    {'error': 'No role assigned'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if role is active
            if not request.user.role.is_active:
                return JsonResponse(
                    {'error': 'Role is inactive'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if role has permission for the URL
            if not request.user.role.has_permission(url_to_check):
                return JsonResponse(
                    {'error': 'Permission denied for this endpoint'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator 