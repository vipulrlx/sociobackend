from django.contrib import admin
from accounts.models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'designation', 'department', 'joining_date', 'email', 'contact_number','country_code', 'created_at')
    list_filter = ('department', 'designation', 'joining_date', 'created_at','country_code',)
    search_fields = ('name', 'designation', 'department', 'user__email','contact_number')
    readonly_fields = ('employee_id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('employee_id', 'user', 'name', 'designation', 'department', 'contact_number', 'country_code')
        }),
        ('Employment Details', {
            'fields': ('joining_date',)
        }),
        ('Media', {
            'fields': ('photo', 'resume')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def email(self, obj):
        return obj.email
    email.short_description = 'Email'