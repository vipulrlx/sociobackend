from rest_framework import generics
from web.models.product import Product
from web.api.serializers.product_serializer import ProductSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related('business').all()
    serializer_class = ProductSerializer


class ProductRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer