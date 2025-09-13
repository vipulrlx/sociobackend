from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "status", "role", "device_token_key")

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("email", "status", "role", "device_token_key")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form  = CustomUserCreationForm
    form      = CustomUserChangeForm
    list_display = (
        "id", "email", "status", "role", "is_staff", "created_at",
    )
    list_filter  = ("status", "role", "is_staff")
    search_fields = ("email",)
    ordering      = ("-created_at",)
    readonly_fields = ("created_at", "last_login")
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Role & Status', {
            'fields': ('role', 'status', 'is_staff', 'is_superuser'),
            'classes': ('collapse',)
        }),
        ('Django Permissions', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Device Token', {
            'fields': ('device_token_key',),
            'classes': ('collapse',)
        }),
        ('Important dates', {
            'fields': ('created_at', 'last_login'),
            'classes': ('collapse',)
        }),
    )
