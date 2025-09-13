from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Q
from accounts.models import User, Role
from accounts.permissions import RoleBasedPermission
from .auth import get_user_phone


@api_view(['GET'])
@permission_classes([IsAuthenticated, RoleBasedPermission])
def user_list_view(request):
    """
    Get list of users with pagination and search
    Excludes users with role=Student
    """
    try:
        # Get query parameters
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        search = request.GET.get('search', '').strip()
        
        # Base queryset - exclude users with Student role
        queryset = User.objects.exclude(
            role__name='Student'
        ).select_related('role').order_by('-created_at')
        
        # Apply search filter if provided
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(role__name__icontains=search)
            )
        
        # Pagination
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        # Prepare response data
        users_data = []
        for user in page_obj:
            users_data.append({
                'id': user.id,
                'email': user.email,
                'phone': get_user_phone(user) or 'N/A',
                'role_name': user.get_role_name(),
                'role_id': user.role.id if user.role else None,
                'status': user.status,
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            })
        
        # Pagination info
        pagination_data = {
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
            'total_count': paginator.count,
            'page_size': page_size,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
        }
        
        return Response({
            'success': True,
            'users': users_data,
            'pagination': pagination_data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated, RoleBasedPermission])
def role_list_view(request):
    """
    Get list of all active roles
    """
    try:
        roles = Role.objects.filter(is_active=True).order_by('name')
        
        roles_data = []
        for role in roles:
            roles_data.append({
                'id': role.id,
                'name': role.name,
                'description': role.description,
                'is_active': role.is_active,
            })
        
        return Response({
            'success': True,
            'roles': roles_data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated, RoleBasedPermission])
def assign_role_view(request, user_id):
    """
    Assign a role to a user
    """
    try:
        user = User.objects.get(id=user_id)
        role_id = request.data.get('role_id')
        
        if not role_id:
            return Response({
                'success': False,
                'message': 'Role ID is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            role = Role.objects.get(id=role_id, is_active=True)
        except Role.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Role not found or inactive'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Update user's role
        user.role = role
        user.save(update_fields=['role'])
        
        return Response({
            'success': True,
            'message': f'Role "{role.name}" assigned successfully to user {user.email}',
            'user': {
                'id': user.id,
                'email': user.email,
                'role_name': user.get_role_name(),
                'role_id': user.role.id if user.role else None,
            }
        })
        
    except User.DoesNotExist:
        return Response({
            'success': False,
            'message': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 