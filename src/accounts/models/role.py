from django.db import models
import re

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, help_text="Description of the role")
    permissions = models.ManyToManyField("accounts.Permission", blank=True, related_name="roles")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'roles'
        ordering = ['name']

    def __str__(self):
        return self.name

    def has_permission(self, url):
        """
        Check if the role has permission for a specific URL
        """
        # Normalize the URL for comparison
        normalized_url = self._normalize_url(url)
        
        # Get all active permissions for this role
        role_permissions = self.permissions.filter(is_active=True)
        
        for permission in role_permissions:
            permission_url = self._normalize_url(permission.url)
            
            # First try exact match
            if normalized_url == permission_url:
                return True
            
            # Try with leading slash variations
            if not normalized_url.startswith('/'):
                if f'/{normalized_url}' == permission_url:
                    return True
            if normalized_url.startswith('/'):
                if normalized_url[1:] == permission_url:
                    return True
            
            # Try with trailing slash variations
            if not normalized_url.endswith('/'):
                if f'{normalized_url}/' == permission_url:
                    return True
            if normalized_url.endswith('/'):
                if normalized_url[:-1] == permission_url:
                    return True
            
            # Try pattern matching for dynamic URLs
            if self._matches_pattern(normalized_url, permission_url):
                return True
        
        return False
    
    def _normalize_url(self, url):
        """
        Normalize URL for comparison by removing leading/trailing slashes
        """
        return url.strip('/')
    
    def _matches_pattern(self, actual_url, pattern_url):
        """
        Check if an actual URL matches a pattern URL that may contain parameters.
        Examples:
        - actual_url: "employees/16" should match pattern_url: "employees/<int:employee_id>"
        - actual_url: "employees/16/edit" should match pattern_url: "employees/<int:employee_id>/edit"
        """
        # If pattern doesn't contain parameters, use exact match
        if '<' not in pattern_url and '>' not in pattern_url:
            return actual_url == pattern_url
        
        # Convert Django URL pattern to regex
        regex_pattern = self._convert_pattern_to_regex(pattern_url)
        
        # Add start and end anchors
        regex_pattern = f'^{regex_pattern}$'
        
        # Test the match
        try:
            return bool(re.match(regex_pattern, actual_url))
        except re.error:
            # If regex is invalid, fall back to exact match
            return actual_url == pattern_url
    
    def _convert_pattern_to_regex(self, pattern):
        """
        Convert Django URL pattern to regex pattern.
        Examples:
        - "employees/<int:employee_id>" -> "employees/([0-9]+)"
        - "employees/<str:name>" -> "employees/([^/]+)"
        - "employees/<slug:slug>" -> "employees/([a-z0-9_-]+)"
        """
        # Replace Django URL patterns with regex patterns
        pattern = re.sub(r'<int:([^>]+)>', r'([0-9]+)', pattern)
        pattern = re.sub(r'<str:([^>]+)>', r'([^/]+)', pattern)
        pattern = re.sub(r'<slug:([^>]+)>', r'([a-z0-9_-]+)', pattern)
        pattern = re.sub(r'<path:([^>]+)>', r'(.+)', pattern)
        pattern = re.sub(r'<uuid:([^>]+)>', r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', pattern)
        
        # Handle generic patterns without type specification
        pattern = re.sub(r'<([^:>]+)>', r'([^/]+)', pattern)
        
        return pattern
