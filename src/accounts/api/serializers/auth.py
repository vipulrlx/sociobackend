from rest_framework import serializers
from accounts.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    platform = serializers.CharField(required=False, default='web')
    category = serializers.CharField(required=False)
    contact_number = serializers.CharField(required=False, max_length=20)
    country_code = serializers.CharField(required=False, default="+91")
    name = serializers.CharField(required=False)
    initialsetup = serializers.CharField(required=False, default="1")

    class Meta:
        model = User
        fields = ("email", "contact_number", "password", "device_token_key", "platform", "category", "country_code", "name")

    def create(self, validated_data):
        platform = validated_data.pop('platform', 'web')
        category = validated_data.pop('category', None)
        name = validated_data.pop('name', None)
        contact_number = validated_data.pop('contact_number', '')
        country_code = validated_data.pop('country_code', '+91')
        
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            device_token_key=validated_data.get("device_token_key"),
        )
        
        from ..views.auth import create_user_profile
        create_user_profile(user, platform, name=name, category=category, phone=contact_number, country_code=country_code)
        
        # Store platform and name in user instance for response
        user._platform = platform
        user._name = name
        
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Import helper functions from auth views
        from ..views.auth import get_user_phone, get_user_name, get_user_country_code, get_user_photo_url
        
        # Get all user profile data using helper functions
        data['contact_number'] = get_user_phone(instance)
        data['country_code'] = get_user_country_code(instance)
        data['name'] = get_user_name(instance)
        data['status'] = instance.status
        
        # Include platform in response if available
        if hasattr(instance, '_platform'):
            data['platform'] = instance._platform
        
        # Include name in response if available
        if hasattr(instance, '_name'):
            data['name'] = instance._name

        # Determine user type
        user_type = "other"
        if hasattr(instance, 'employees') and instance.employees.exists():
            user_type = "employee"
        elif hasattr(instance, 'students') and instance.students.exists():
            user_type = "student"
        data['user_type'] = user_type
        
        # Get photo_url if request context is available
        request = self.context.get('request')
        if request:
            data['photo_url'] = get_user_photo_url(instance, request)
        else:
            data['photo_url'] = None
        
        return data
