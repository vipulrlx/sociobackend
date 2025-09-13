from django.core.management.base import BaseCommand
from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver
from accounts.models import Permission
from accounts.permissions import RoleBasedPermission
import re


class Command(BaseCommand):
    help = 'Sync URL endpoints to the Permission model (only for URLs with RoleBasedPermission or function-based views that need permissions)'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configuration for the command
        self.config = {
            'custom_apps': ['accounts', 'web', 'app_settings'],
            'url_parameter_pattern': r'<[^>]+>',  # Regex to match URL parameters like <int:pk>, <str:name>, etc.
        }

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating records',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update existing permissions with new names',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force_update = options['force']
        
        self.stdout.write(
            self.style.SUCCESS('Starting permission sync (RoleBasedPermission + function-based views)...')
        )
        
        # Get all URL patterns with their views
        url_patterns_with_views = self.get_url_patterns_with_views()
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        for url_pattern, view_class, view_func in url_patterns_with_views:
            if dry_run:
                view_name = view_class.__name__ if view_class else (view_func.__name__ if view_func else 'None')
                self.stdout.write(f"Would process: {url_pattern} (View: {view_name})")
                continue
                
            result = self.process_url_pattern(url_pattern, view_class, view_func, force_update)
            if result == 'created':
                created_count += 1
            elif result == 'updated':
                updated_count += 1
            else:
                skipped_count += 1
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'DRY RUN: Would process {len(url_patterns_with_views)} URL patterns')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Permission sync completed!\n'
                    f'Created: {created_count}\n'
                    f'Updated: {updated_count}\n'
                    f'Skipped: {skipped_count}\n'
                    f'Total processed: {len(url_patterns_with_views)}'
                )
            )

    def get_url_patterns_with_views(self):
        """
        Extract URL patterns with their view classes and functions, only from custom apps.
        """
        url_patterns_with_views = []
        
        # Get the main URL resolver
        resolver = get_resolver()
        
        def extract_patterns(patterns, base_path='', app_name=''):
            for pattern in patterns:
                if isinstance(pattern, URLPattern):
                    # Get the full URL path
                    pattern_str = str(pattern.pattern)
                    full_path = base_path + pattern_str
                    
                    # Handle empty pattern (root URL)
                    if pattern_str == '' and base_path == '':
                        full_path = '/'
                    
                    # Skip public URLs
                    if self.is_public_url(full_path):
                        continue
                    
                    # Clean up the path using generic methods
                    full_path = self.clean_url_path(full_path)
                    
                    # Only include valid paths
                    if self.is_valid_url_path(full_path):
                        # Get the view class and function from the pattern
                        view_class = self.get_view_class(pattern)
                        view_func = self.get_view_function(pattern)
                        url_patterns_with_views.append((full_path, view_class, view_func))
                        
                elif isinstance(pattern, URLResolver):
                    # Only process URL resolvers for our custom apps
                    new_base = base_path + str(pattern.pattern)
                    
                    # Check if this resolver is for one of our custom apps
                    resolver_app = self.get_resolver_app_name(pattern)
                    if resolver_app in self.config['custom_apps'] or not resolver_app:
                        extract_patterns(pattern.url_patterns, new_base, resolver_app)
        
        extract_patterns(resolver.url_patterns)
        return list(set(url_patterns_with_views))  # Remove duplicates

    def is_public_url(self, url_path):
        """
        Check if a URL is public and should be excluded from permission creation.
        """
        # Define public patterns that should be excluded
        public_patterns = [
            # Authentication endpoints
            'login', 'register', 'logout', 'change-password',
            'auth/login', 'auth/register', 'auth/logout', 'auth/refresh',
            'auth/google', 'auth/change-password', 'api/v1/menu/list', 'api/v1/user/details',
            # Django system URLs
            'admin', 'static', 'media', 'jsi18n', 'autocomplete',
            'password_change', 'social_django', 'token_blacklist', 'auth/group',
        ]
        
        # Check if URL contains any public pattern
        for pattern in public_patterns:
            if pattern in url_path:
                return True
        
        return False

    def get_view_class(self, pattern):
        """
        Extract the view class from a URL pattern.
        """
        try:
            if hasattr(pattern, 'callback'):
                # For class-based views
                if hasattr(pattern.callback, 'view_class'):
                    return pattern.callback.view_class
                # For function-based views, we can't easily get the class
                # but we can check if it's a method of a class
                elif hasattr(pattern.callback, '__self__'):
                    return pattern.callback.__self__.__class__
                else:
                    # For function-based views, return None
                    return None
        except:
            pass
        return None

    def get_view_function(self, pattern):
        """
        Extract the view function from a URL pattern.
        """
        try:
            if hasattr(pattern, 'callback'):
                # For function-based views
                if callable(pattern.callback) and not hasattr(pattern.callback, 'view_class'):
                    return pattern.callback
        except:
            pass
        return None

    def has_role_based_permission(self, view_class):
        """
        Check if a view class has RoleBasedPermission in its permission_classes.
        """
        if not view_class:
            return False
        
        try:
            # Check if the view has permission_classes attribute
            if hasattr(view_class, 'permission_classes'):
                permission_classes = view_class.permission_classes
                
                # Check if RoleBasedPermission is in the permission classes
                if RoleBasedPermission in permission_classes:
                    return True
                
                # Also check for string references (in case of lazy loading)
                permission_class_names = [cls.__name__ if hasattr(cls, '__name__') else str(cls) for cls in permission_classes]
                if 'RoleBasedPermission' in permission_class_names:
                    return True
            
            # Check parent classes for permission_classes
            for parent_class in view_class.__mro__[1:]:  # Skip the class itself
                if hasattr(parent_class, 'permission_classes'):
                    permission_classes = parent_class.permission_classes
                    
                    if RoleBasedPermission in permission_classes:
                        return True
                    
                    permission_class_names = [cls.__name__ if hasattr(cls, '__name__') else str(cls) for cls in permission_classes]
                    if 'RoleBasedPermission' in permission_class_names:
                        return True
                        
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Error checking permissions for {view_class}: {str(e)}')
            )
        
        return False

    def needs_permission(self, view_class, view_func, url_path):
        """
        Check if a view needs permission based on various criteria.
        """
        # Class-based views with RoleBasedPermission
        if view_class and self.has_role_based_permission(view_class):
            return True
        
        # Class-based views without permission_classes but need permissions
        if view_class and not view_func:
            # Check if it's a web view (not API) that needs permissions
            if not url_path.startswith('/api/') and not self.is_public_url(url_path):
                # Check the class name for dashboard or other protected views
                class_name = view_class.__name__.lower()
                protected_keywords = ['dashboard', 'create', 'edit', 'delete', 'update', 'manage', 'list', 'detail']
                if any(keyword in class_name for keyword in protected_keywords):
                    return True
                
                # Check if it's in the web app and not a public endpoint
                if 'web' in str(view_class.__module__):
                    return True
        
        # Function-based views that are not public
        if view_func and not view_class:
            # Check if it's a web view (not API) that needs permissions
            if not url_path.startswith('/api/') and not self.is_public_url(url_path):
                # Check if the function name suggests it needs permissions
                func_name = view_func.__name__.lower()
                permission_keywords = ['create', 'edit', 'delete', 'update', 'manage', 'list', 'detail']
                if any(keyword in func_name for keyword in permission_keywords):
                    return True
                
                # Check if it's in the web app and not a public endpoint
                if 'web' in str(view_func.__module__):
                    return True
        
        return False

    def clean_url_path(self, url_path):
        """
        Clean up URL path while preserving URL parameters for pattern matching.
        """
        # Preserve root URL
        if url_path == '/':
            return '/'
        
        # Don't remove URL parameters - keep them for pattern matching
        # This allows permissions to work with dynamic URLs like /employees/16/edit/
        
        # Clean up multiple slashes but preserve the structure
        url_path = re.sub(r'/+', '/', url_path)
        url_path = url_path.rstrip('/')
        
        return url_path

    def is_valid_url_path(self, url_path):
        """
        Check if a URL path is valid for permission creation.
        """
        if not url_path:
            return False
        
        # Allow root URL "/"
        if url_path == '/':
            return True
        
        # Skip Django admin URLs
        if url_path.startswith('admin/') or 'admin' in url_path:
            return False
        
        return True

    def get_resolver_app_name(self, resolver):
        """
        Try to determine the app name from a URL resolver.
        """
        try:
            # Check if the resolver has a url_patterns attribute
            if hasattr(resolver, 'url_patterns'):
                # Look for patterns that might indicate the app
                for pattern in resolver.url_patterns:
                    if hasattr(pattern, 'callback'):
                        if hasattr(pattern.callback, '__module__'):
                            module = pattern.callback.__module__
                            if 'accounts.' in module:
                                return 'accounts'
                            elif 'web.' in module:
                                return 'web'
                            elif 'app_settings.' in module:
                                return 'app_settings'
        except:
            pass
        return None

    def process_url_pattern(self, url_pattern, view_class, view_func, force_update=False):
        """
        Process a single URL pattern and create/update the Permission record if it needs permissions.
        """
        try:
            # Check if the view needs permission
            if not self.needs_permission(view_class, view_func, url_pattern):
                self.stdout.write(
                    self.style.WARNING(f'Skipped (no permission needed): {url_pattern}')
                )
                return 'skipped'
            
            # Generate permission name from URL
            permission_name = self.generate_permission_name(url_pattern)
            
            # Check if permission already exists
            permission, created = Permission.objects.get_or_create(
                url=url_pattern,
                defaults={
                    'name': permission_name,
                    'description': f'Permission for endpoint: {url_pattern}',
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created permission: {permission_name} for {url_pattern}')
                )
                return 'created'
            else:
                # Permission already exists
                if force_update:
                    old_name = permission.name
                    permission.name = permission_name
                    permission.save()
                    self.stdout.write(
                        self.style.WARNING(f'Updated permission: {old_name} -> {permission_name} for {url_pattern}')
                    )
                    return 'updated'
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Skipped existing permission: {permission.name} for {url_pattern}')
                    )
                    return 'skipped'
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing {url_pattern}: {str(e)}')
            )
            return 'error'

    def generate_permission_name(self, url_pattern):
        """
        Generate a human-readable permission name from the URL pattern.
        """
        if not url_pattern:
            return 'root'
        
        # Remove leading and trailing slashes
        url_path = url_pattern.strip('/')
        
        # Split by slashes and filter out empty strings
        parts = [part for part in url_path.split('/') if part]
        
        if not parts:
            return 'root'
        
        # Handle different URL patterns
        if len(parts) >= 3 and parts[0] == 'api' and parts[1] == 'v1':
            # For API v1 URLs: /api/v1/employee/create/ -> employee_create
            return '_'.join(parts[2:])
        elif len(parts) >= 2 and parts[0] == 'api':
            # For API URLs: /api/something/ -> something
            return '_'.join(parts[1:])
        else:
            # For other URLs (web app URLs), use all parts
            return '_'.join(parts) 
