from django.contrib import admin
from accounts.models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'dob', 'gender', 'enrollment_date', 'contact_number', 'country_code')
    list_filter = ('gender', 'enrollment_date', 'dob', 'country_code')
    search_fields = ('full_name', 'user__email', 'contact_number')
    #readonly_fields = ('user',)
    ordering = ('full_name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'full_name', 'dob', 'gender', 'contact_number', 'country_code')
        }),
        ('Enrollment Details', {
            'fields': ('enrollment_date',)
        }),
    ) 