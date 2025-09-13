from django.db import models


class Permission(models.Model):
    """
    Model to store endpoint URLs with their descriptions.
    Used for managing API permissions and access control.
    """
    url = models.CharField(max_length=255, unique=True, help_text="The endpoint URL path")
    name = models.CharField(max_length=255, help_text="Human-readable name for the permission")
    description = models.TextField(blank=True, help_text="Detailed description of what this endpoint does")
    is_active = models.BooleanField(default=True, help_text="Whether this permission is currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'permissions'
        ordering = ['url']
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'

    def __str__(self):
        return f"{self.name} ({self.url})"

    def get_permission_name(self):
        """
        Generate a permission name based on the URL suffix.
        Example: /api/v1/employee/create/ -> employee_create
        """
        if not self.url:
            return self.name
        
        # Remove leading and trailing slashes
        url_path = self.url.strip('/')
        
        # Split by slashes and filter out empty strings
        parts = [part for part in url_path.split('/') if part]
        
        # If we have parts, use the last meaningful parts
        if len(parts) >= 2:
            # For URLs like /api/v1/employee/create/, use employee_create
            if len(parts) >= 3 and parts[0] in ['api', 'v1']:
                return '_'.join(parts[2:])
            else:
                return '_'.join(parts)
        elif len(parts) == 1:
            return parts[0]
        else:
            return 'root' 
