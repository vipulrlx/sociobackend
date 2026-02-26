from django.db import models
from django.conf import settings


class Lead(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
        ("closed", "Closed"),
        ("lost", "Lost"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leads",
        default=1
    )

    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)

    source = models.CharField(max_length=100, default="manual")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    zoho_lead_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class LeadFollowUp(models.Model):
    FOLLOWUP_TYPE = [
        ("note", "Note"),
        ("call", "Call"),
        ("email", "Email"),
        ("ai_call", "AI Call"),
    ]

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="followups"
    )

    followup_type = models.CharField(max_length=20, choices=FOLLOWUP_TYPE)
    notes = models.TextField(blank=True, null=True)
    conversation_json = models.JSONField(blank=True, null=True)

    next_followup_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

class LeadCallLog(models.Model):
    CALL_STATUS = [
        ("initiated", "Initiated"),
        ("ringing", "Ringing"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="call_logs"
    )

    call_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=30, choices=CALL_STATUS, default="initiated")
    raw_response = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)