from django.db import models
from django.utils import timezone
from .user import User

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    contact_number = models.CharField(max_length=100, null=True, blank=True)
    country_code = models.CharField(max_length=5, default="+91", blank=True)
    joining_date = models.DateField()
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    resume = models.FileField(upload_to='employee_resumes/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employee'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.name} - {self.designation}"

    @property
    def email(self):
        return self.user.email if self.user else None