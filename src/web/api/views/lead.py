from rest_framework import generics
from web.models.lead import Lead
from web.api.serializers.lead_serializer import LeadSerializer

class LeadListView(generics.ListAPIView):
    queryset = Lead.objects.prefetch_related('calls').all().order_by('-created_at')
    serializer_class = LeadSerializer


class LeadDetailView(generics.RetrieveAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer