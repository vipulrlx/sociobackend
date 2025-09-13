from rest_framework import serializers
from .models import AppSettings, AppMedia


class AppMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppMedia
        fields = ['id', 'kind', 'title', 'file', 'url', 'thumbnail', 'order', 'is_active']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and instance.file:
            data['file'] = request.build_absolute_uri(instance.file.url)
        if request and instance.thumbnail:
            data['thumbnail'] = request.build_absolute_uri(instance.thumbnail.url)
        return data


class AppSettingsSerializer(serializers.ModelSerializer):
    media = AppMediaSerializer(many=True, read_only=True)

    class Meta:
        model = AppSettings
        fields = ['name', 'description', 'logo', 'terms', 'updated_at', 'media']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and instance.logo:
            data['logo'] = request.build_absolute_uri(instance.logo.url)
        return data 