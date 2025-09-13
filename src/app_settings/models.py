from django.db import models
from django.core.exceptions import ValidationError


class AppSettings(models.Model):
    name = models.CharField(max_length=200)
    appversion = models.CharField(max_length=200, blank=True, null=True)
    platform = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="settings/logo/", blank=True, null=True)
    terms = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "App Settings"
        verbose_name_plural = "App Settings"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'name': 'ISTI',
                'description': '',
                'terms': ''
            }
        )
        return obj


class AppMedia(models.Model):
    KIND_CHOICES = [
        ('MP4', 'MP4'),
        ('YOUTUBE', 'YouTube'),
    ]

    app_settings = models.ForeignKey(
        AppSettings,
        on_delete=models.CASCADE,
        related_name='media'
    )
    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    title = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to="settings/videos/", blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to="settings/thumbnails/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_at"]
        verbose_name = "App Media"
        verbose_name_plural = "App Media"

    def __str__(self):
        return f"{self.title} ({self.kind})"

    def clean(self):
        if self.kind == 'MP4':
            if not self.file:
                raise ValidationError("File is required for MP4 media")
            if self.url:
                raise ValidationError("URL should be empty for MP4 media")
        elif self.kind == 'YOUTUBE':
            if not self.url:
                raise ValidationError("URL is required for YouTube media")
            if self.file:
                raise ValidationError("File should be empty for YouTube media")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs) 