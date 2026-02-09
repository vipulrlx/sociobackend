from django.db import models
from django.conf import settings

class Brand(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="brands"
    )
    website = models.URLField(max_length=500, unique=True, db_index=True)
    entity_type = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    industry = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    analysis_data = models.JSONField()

    # 🎨 Brand visual styles
    photography_style = models.CharField(max_length=255, blank=True, null=True)
    font_style = models.CharField(max_length=255, blank=True, null=True)
    filter_style = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "website")

    def __str__(self):
        return f"{self.user_id} - {self.website}"