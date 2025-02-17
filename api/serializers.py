from rest_framework import serializers
from .models import ApiKey, ApiLog


class ApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiKey
        fields = ['id', 'user', 'key', 'date_created', 'is_active']


class ApiLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiLog
        fields = ['id', 'user', 'action', 'request_payload', 'response_payload', 'timestamp']
