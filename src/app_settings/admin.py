from django.contrib import admin
from .models import AppSettings, AppMedia


class AppMediaInline(admin.TabularInline):
    model = AppMedia
    extra = 0
    fields = ['kind', 'title', 'file', 'url', 'thumbnail', 'order', 'is_active']


@admin.register(AppSettings)
class AppSettingsAdmin(admin.ModelAdmin):
    list_display = ['name', 'updated_at']
    readonly_fields = ['updated_at']
    inlines = [AppMediaInline]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AppMedia)
class AppMediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'kind', 'order', 'is_active']
    list_filter = ['kind', 'is_active']
    search_fields = ['title', 'url']
    ordering = ['order', 'created_at']
    fields = ['app_settings', 'kind', 'title', 'file', 'url', 'thumbnail', 'order', 'is_active']