from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from accounts.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import json

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define public URLs that don't require authentication
        public_urls = [
            '/login/',
            '/register/',
            '/logout/',
            '/api/v1/auth/login/',
            '/api/v1/auth/register/',
            '/api/v1/auth/google/',
            '/api/v1/auth/refresh/',
            '/api/v1/auth/forgot-password/',
            '/api/v1/auth/reset-password/',
            '/admin/',
            '/static/',
            '/media/',
        ]
        
        # Check if the current path is public
        is_public = any(request.path.startswith(url) for url in public_urls)
        
        if is_public:
            return self.get_response(request)
        
        # For API requests, let them handle authentication themselves
        if request.path.startswith('/api/'):
            return self.get_response(request)
        
        token = None
        
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        if not token:
            token = request.COOKIES.get('access_token')
        
        # If no token found, redirect to login
        if not token:
            if request.path == '/':
                return redirect('web:login')
            return redirect('web:login')
        
        try:
            # Verify the token using SimpleJWT
            access_token = AccessToken(token)
            payload = access_token.payload
            user_id = payload.get('user_id')
            
            if not user_id:
                raise InvalidToken("No user_id in token")
            
            try:
                user = User.objects.get(id=user_id, status=User.Status.ACTIVE)
                request.user = user
                
                # Check permissions for non-public URLs
                if not is_public and not request.path.startswith('/api/'):
                    # For web views, check if user has role and permission
                    if not user.is_superuser and user.role:
                        if not user.role.is_active:
                            return redirect('web:login')
                        
                        # Check if role has permission for the current path
                        if not user.role.has_permission(request.path):
                            return JsonResponse(
                                {'error': 'Permission denied'}, 
                                status=403
                            )
                    elif not user.is_superuser and not user.role:
                        return JsonResponse(
                            {'error': 'No role assigned'}, 
                            status=403
                        )
                        
            except User.DoesNotExist:
                raise InvalidToken("User not found or inactive")
                
        except (InvalidToken, TokenError):
            # Token is invalid or expired
            if request.path == '/':
                return redirect('web:login')
            return redirect('web:login')
        
        response = self.get_response(request)
        
        # Add cache control headers to prevent back button issues
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        return response 