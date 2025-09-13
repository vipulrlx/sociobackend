from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra):
        if not email:
            raise ValueError("Email required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra):
        extra.setdefault("status", User.Status.ACTIVE)
        return self._create_user(email, password, **extra)

    def create_superuser(self, email, password, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra)

class User(AbstractBaseUser, PermissionsMixin):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        DISABLED = "disabled", "Disabled"
        SUSPENDED = "suspended", "Suspended"

    id = models.AutoField(primary_key=True)                # user_id INT(11)
    email = models.EmailField(max_length=100, unique=True)
    device_token_key = models.CharField(max_length=500, blank=True, null=True)  # For mobile app notifications
    role = models.ForeignKey("accounts.Role", null=True, blank=True,
                             on_delete=models.SET_NULL)
    status = models.CharField(max_length=10,
                              choices=Status.choices,
                              default=Status.ACTIVE)
    created_at = models.DateTimeField(default=timezone.now)

    # Django internals
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    def has_permission(self, url):
        """
        Check if user has permission for a specific URL
        """
        # Superuser has all permissions
        if self.is_superuser:
            return True
        
        # Check if user has a role
        if not self.role:
            return False
        
        # Check if role is active
        if not self.role.is_active:
            return False
        
        # Check if role has permission for the URL
        return self.role.has_permission(url)

    def get_role_name(self):
        """
        Get the name of the user's role
        """
        return self.role.name if self.role else "No Role"