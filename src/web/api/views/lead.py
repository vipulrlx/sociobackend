from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone

from web.models.lead import Lead, LeadFollowUp, LeadCallLog
from web.api.serializers.lead_serializer import LeadSerializer, LeadFollowUpSerializer
from web.services.elevenlabs import start_ai_call

class CreateLeadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id

        serializer = LeadSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        lead = serializer.save(user=request.user)

        # optional followup
        followup_note = request.data.get("followup_note")
        if followup_note:
            LeadFollowUp.objects.create(
                lead=lead,
                followup_type="note",
                notes=followup_note
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UpdateLeadView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, lead_id):
        try:
            lead = Lead.objects.get(id=lead_id, user=request.user)
        except Lead.DoesNotExist:
            return Response({"error": "Lead not found"}, status=404)

        serializer = LeadSerializer(
            lead,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class AddLeadFollowupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lead_id):
        try:
            lead = Lead.objects.get(id=lead_id, user=request.user)
        except Lead.DoesNotExist:
            return Response({"error": "Lead not found"}, status=404)

        data = request.data.copy()
        data["lead"] = lead.id

        serializer = LeadFollowUpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class ZohoLeadWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data

        # map Zoho fields safely
        lead = Lead.objects.create(
            name=data.get("Full_Name") or data.get("Last_Name"),
            email=data.get("Email"),
            phone=data.get("Phone"),
            company=data.get("Company"),
            source="zoho",
            zoho_lead_id=data.get("id"),
            user_id=data.get("user_id")  # you may map properly
        )

        return Response({"status": "success"})

class LeadListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        leads = Lead.objects.filter(user=request.user).order_by("-created_at")
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data)

class LeadDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, lead_id):
        try:
            lead = Lead.objects.get(id=lead_id, user=request.user)
        except Lead.DoesNotExist:
            return Response({"error": "Lead not found"}, status=404)

        lead_data = LeadSerializer(lead).data
        followups = LeadFollowUp.objects.filter(lead=lead).order_by("-created_at")
        calls = lead.call_logs.all().order_by("-created_at")

        lead_data["followups"] = LeadFollowUpSerializer(followups, many=True).data
        lead_data["call_logs"] = [
            {
                "id": c.id,
                "call_id": c.call_id,
                "status": c.status,
                "created_at": c.created_at,
            }
            for c in calls
        ]

        return Response(lead_data)

class InitiateAICallView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lead_id):
        try:
            lead = Lead.objects.get(id=lead_id, user=request.user)
        except Lead.DoesNotExist:
            return Response({"error": "Lead not found"}, status=404)

        # 🔥 create call log first
        call_log = LeadCallLog.objects.create(
            lead=lead,
            status="initiated"
        )

        result = start_ai_call(lead.phone, lead.id)

        call_id = result.get("call_id") or result.get("conversation_id")

        # 🔥 update log with response
        call_log.call_id = call_id
        call_log.raw_response = result
        call_log.save()

        LeadFollowUp.objects.create(
            lead=lead,
            followup_type="ai_call",
            notes="AI call initiated"
        )

        return Response(result)

class ElevenLabsWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    @transaction.atomic
    def post(self, request):
        data = request.data

        metadata = data.get("metadata", {}) or {}
        lead_id = metadata.get("lead_id")
        call_id = data.get("call_id") or data.get("conversation_id")
        status_val = data.get("status", "completed")

        # =========================
        # ✅ CASE 1 — existing lead
        # =========================
        lead = None

        if lead_id:
            lead = Lead.objects.filter(id=lead_id).first()

        # =========================
        # ✅ CASE 2 — inbound call
        # =========================
        if not lead:
            phone = data.get("from_number") or data.get("caller")

            lead = Lead.objects.create(
                name=phone or "Inbound Lead",
                phone=phone or "unknown",
                source="inbound_call",
                user_id=metadata.get("user_id")  # optional mapping
            )

        # =========================
        # ✅ update call log
        # =========================
        if call_id:
            call_log = LeadCallLog.objects.filter(call_id=call_id).first()

            if call_log:
                call_log.status = status_val
                call_log.raw_response = data
                call_log.save()
            else:
                LeadCallLog.objects.create(
                    lead=lead,
                    call_id=call_id,
                    status=status_val,
                    raw_response=data
                )

        # =========================
        # ✅ store followup
        # =========================
        LeadFollowUp.objects.create(
            lead=lead,
            followup_type="ai_call",
            notes=f"AI call {status_val}",
            conversation_json=data
        )

        return Response({"status": "stored"})