from rest_framework import serializers
from web.models.lead import Lead
from web.models.call_log import CallLog

class CallLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = '__all__'


class LeadSerializer(serializers.ModelSerializer):
    calls = CallLogSerializer(many=True, read_only=True)

    class Meta:
        model = Lead
        fields = '__all__'