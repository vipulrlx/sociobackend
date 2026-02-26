from rest_framework import serializers
from web.models.lead import Lead, LeadFollowUp


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = "__all__"
        read_only_fields = ("user",)


class LeadFollowUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadFollowUp
        fields = "__all__"