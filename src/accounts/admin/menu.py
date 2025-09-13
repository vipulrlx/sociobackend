from django.contrib import admin
from accounts.models import Menu, SubMenu

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'category', 'sequence', 'icon', 'destination_url', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'display_name', 'destination_url')
    ordering = ('sequence',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'display_name', 'sequence', 'icon', 'category')
        }),
        ('Navigation', {
            'fields': ('destination_url',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(SubMenu)
class SubMenuAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'parent_menu', 'sequence', 'icon', 'destination_url', 'is_active')
    list_filter = ('parent_menu', 'is_active', 'created_at')
    search_fields = ('name', 'display_name', 'destination_url')
    ordering = ('parent_menu', 'sequence')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('parent_menu', 'name', 'display_name', 'sequence', 'icon')
        }),
        ('Navigation', {
            'fields': ('destination_url',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    ) 