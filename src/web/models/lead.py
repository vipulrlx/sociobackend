from django.db import models

class Lead(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    )

    name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    source = models.CharField(max_length=100, default='elevenlabs')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number