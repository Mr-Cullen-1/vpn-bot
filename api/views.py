from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ApiKey, ApiLog
from .serializers import ApiKeySerializer, ApiLogSerializer


class ApiKeyViewSet(viewsets.ModelViewSet):
    queryset = ApiKey.objects.all()
    serializer_class = ApiKeySerializer
    permission_classes = [IsAuthenticated]  # Защита доступом только для авторизованных пользователей


class ApiLogViewSet(viewsets.ModelViewSet):
    queryset = ApiLog.objects.all()
    serializer_class = ApiLogSerializer
    permission_classes = [IsAuthenticated]  # Защита доступом только для авторизованных пользователей
