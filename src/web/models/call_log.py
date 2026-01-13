from django.db import models
from .lead import Lead

class CallLog(models.Model):
    lead = models.ForeignKey(
        Lead,
        related_name='calls',
        on_delete=models.CASCADE
    )

    call_id = models.CharField(max_length=255, unique=True)
    agent_id = models.CharField(max_length=255)
    call_status = models.CharField(max_length=50)

    call_start_time = models.DateTimeField(null=True, blank=True)
    call_end_time = models.DateTimeField(null=True, blank=True)
    call_duration = models.IntegerField(null=True, blank=True)

    transcript = models.TextField(blank=True, null=True)
    intent = models.CharField(max_length=255, blank=True, null=True)
    sentiment = models.CharField(max_length=50, blank=True, null=True)

    recording_url = models.URLField(blank=True, null=True)

    raw_payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)