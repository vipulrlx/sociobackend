from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from web.models.lead import Lead
from web.models.call_log import CallLog

class ElevenLabsWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data

        phone = data.get('caller', {}).get('phone_number')
        call_id = data.get('call_id')

        if not phone or not call_id:
            return Response({"error": "Invalid payload"}, status=400)

        lead, _ = Lead.objects.get_or_create(
            phone_number=phone,
            defaults={
                "name": data.get('caller', {}).get('name'),
                "email": data.get('caller', {}).get('email')
            }
        )

        CallLog.objects.update_or_create(
            call_id=call_id,
            defaults={
                "lead": lead,
                "agent_id": data.get('agent_id'),
                "call_status": data.get('status'),
                "call_start_time": data.get('started_at'),
                "call_end_time": data.get('ended_at'),
                "call_duration": data.get('duration'),
                "transcript": data.get('transcript'),
                "intent": data.get('intent'),
                "sentiment": data.get('sentiment'),
                "recording_url": data.get('recording_url'),
                "raw_payload": data
            }
        )

        return Response({"success": True})