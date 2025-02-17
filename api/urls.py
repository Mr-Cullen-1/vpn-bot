from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApiKeyViewSet, ApiLogViewSet

router = DefaultRouter()
router.register(r'api_keys', ApiKeyViewSet)
router.register(r'api_logs', ApiLogViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),  # API базовый путь
]
