from django.db import models
from django.utils import timezone
from .user import User


GENDER_CHOICES = [
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
]


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='students', null=True, blank=True)
    full_name = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=100, null=True, blank=True)
    country_code = models.CharField(max_length=5, default="+91", blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    bio = models.CharField(max_length=500, null=True, blank=True)
    photo = models.ImageField(upload_to='employee_photos/', null=True, blank=True)
    enrollment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name 
