from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class RoleBasedPermission(permissions.BasePermission):
    """
    Custom permission class to check role-based permissions
    """
    
    def has_permission(self, request, view):
        # Allow public endpoints
        public_urls = [
            '/api/v1/auth/login/',
            '/api/v1/auth/register/',
            '/api/v1/auth/google/',
            '/api/v1/auth/refresh/'
        ]
        
        if request.path in public_urls:
            return True
        
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Superuser bypass all permissions
        if request.user.is_superuser:
            return True
        
        # Check if user has a role
        if not request.user.role:
            raise PermissionDenied("No role assigned to user")
        
        # Check if role is active
        if not request.user.role.is_active:
            raise PermissionDenied("User role is inactive")
        
        # Check if role has permission for the URL
        if not request.user.role.has_permission(request.path):
            raise PermissionDenied("Permission denied for this endpoint")
        
        return True

    def has_object_permission(self, request, view, obj):
        # For object-level permissions, use the same logic as has_permission
        return self.has_permission(request, view) 
