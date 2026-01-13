from rest_framework import serializers
from web.models.product import Product

class ProductSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(
        source='business.company_name',
        read_only=True
    )

    class Meta:
        model = Product
        fields = '__all__'