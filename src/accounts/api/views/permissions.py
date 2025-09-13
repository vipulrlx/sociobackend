from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from accounts.permissions import RoleBasedPermission

class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission]
    
    def get(self, request):
        """
        Get current user's role and permissions
        """
        try:
            user = request.user
            
            if not user.role:
                return Response({
                    "success": False,
                    "message": "No role assigned to user",
                    "role": None,
                    "permissions": []
                }, status=status.HTTP_403_FORBIDDEN)
            
            permissions = user.role.permissions.filter(is_active=True)
            
            return Response({
                "success": True,
                "role": {
                    "id": user.role.id,
                    "name": user.role.name,
                    "description": user.role.description,
                    "is_active": user.role.is_active
                },
                "permissions": [
                    {
                        "id": perm.id,
                        "url": perm.url,
                        "name": perm.name,
                        "description": perm.description
                    }
                    for perm in permissions
                ]
            })
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Failed to fetch user permissions: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CheckPermissionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Check if user has permission for a specific URL
        """
        try:
            url = request.data.get('url')
            
            if not url:
                return Response({
                    "success": False,
                    "message": "URL is required"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            has_permission = request.user.has_permission(url)
            
            return Response({
                "success": True,
                "url": url,
                "has_permission": has_permission,
                "role": request.user.get_role_name()
            })
        except Exception as e:
            return Response({
                "success": False,
                "message": f"Failed to check permission: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
