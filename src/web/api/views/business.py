from rest_framework import generics
from web.models.business import Business
from web.api.serializers.business_serializer import BusinessSerializer

class BusinessListCreateView(generics.ListCreateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer


class BusinessRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer