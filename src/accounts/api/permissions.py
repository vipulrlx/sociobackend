from rest_framework.permissions import BasePermission

class HasRole(BasePermission):
    role_name = ""

    def has_permission(self, request, view):
        return request.user.roles.filter(name=self.role_name).exists()
    