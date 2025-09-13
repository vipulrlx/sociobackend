from django.db import models
from django.utils import timezone
from .user import User

class Onetimepassword(models.Model):
    onetimepassword_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    otp = models.CharField(max_length=10)
    service = models.CharField(max_length=100)
    sent_time = models.DateTimeField(null=True, blank=True)
    sequence_no = models.IntegerField(default=0)
    via_sms = models.IntegerField(default=0)
    via_email = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'onetimepassword'
        verbose_name = 'Onetimepassword'

    def __str__(self):
        return f"{self.otp}"