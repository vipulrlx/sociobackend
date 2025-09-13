from rest_framework import serializers
from accounts.models import Menu, SubMenu

class SubMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMenu
        fields = ['id', 'name', 'display_name', 'sequence', 'icon', 'destination_url', 'is_active']

class MenuSerializer(serializers.ModelSerializer):
    submenus = SubMenuSerializer(many=True, read_only=True)
    
    class Meta:
        model = Menu
        fields = ['id', 'name', 'display_name', 'sequence', 'icon', 'destination_url', 'category', 'is_active', 'submenus'] 