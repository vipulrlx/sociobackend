from rest_framework import serializers
from accounts.models import Student, User

class StudentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(write_only=True, required=False)
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'student_id', 'user', 'full_name', 'dob', 
            'photo', 'photo_url', 'created_at', 'updated_at',
            'user_email', 'gender', 'contact_number', 'country_code','bio'
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
                'user_email': 'Email address is required to create a student.'
            })
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        validated_data.pop('user_email', None)
        return super().update(instance, validated_data) 