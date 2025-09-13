from rest_framework import serializers
from accounts.models import Employee, User

class EmployeeSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True, required=False)
    photo_url = serializers.SerializerMethodField()
    resume_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'user', 'name', 'designation', 
            'department', 'joining_date', 'photo', 'resume',
            'photo_url', 'resume_url', 'created_at', 'updated_at',
            'user_email', 'gender', 'contact_number', 'birth_date','country_code','bio'
        ]
        read_only_fields = ['employee_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'required': False},
            'photo': {'required': False},
            'resume': {'required': False}
        }
    
    def get_photo_url(self, obj):
        if obj.photo:
            return self.context['request'].build_absolute_uri(obj.photo.url)
        return None
    
    def get_resume_url(self, obj):
        if obj.resume:
            return self.context['request'].build_absolute_uri(obj.resume.url)
        return None
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['email'] = instance.email
        # Phone is now directly from the Employee model, no need to get from user
        return data
    
    def create(self, validated_data):
        user_email = validated_data.pop('user_email', None)
        
        if user_email:
            if User.objects.filter(email=user_email).exists():
                raise serializers.ValidationError({
                    'user_email': 'A user with this email address already exists.'
                })
            
            user = User.objects.create(
                email=user_email,
                status=User.Status.ACTIVE
            )
            validated_data['user'] = user
        else:
            raise serializers.ValidationError({
                'user_email': 'Email address is required to create an employee.'
            })
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data.pop('user_email', None)
        return super().update(instance, validated_data) 