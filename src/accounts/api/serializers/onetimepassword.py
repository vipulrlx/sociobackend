from rest_framework import serializers
from accounts.models import Onetimepassword

class OnetimepasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Onetimepassword
        fields = ['user_id', 'service', 'otp', 'sent_time', 'sequence_no', 'via_sms', 'via_email']
        read_only_fields = ['onetimepassword_id', 'created_at', 'updated_at']
