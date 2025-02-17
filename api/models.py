from django.db import models
from bot_management.models import User, Subscription, Transaction  # Импортируем из bot_management

# Здесь можем хранить API связанные данные или, например, логирование запросов
class ApiLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_logs", verbose_name="Пользователь")
    action = models.CharField(max_length=255, verbose_name="Действие")
    request_payload = models.TextField(verbose_name="Параметры запроса")
    response_payload = models.TextField(verbose_name="Ответ сервера")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время запроса")
    
    class Meta:
        verbose_name = "Лог API"
        verbose_name_plural = "Логи API"

    def __str__(self):
        return f"API запрос от {self.user.username} в {self.timestamp}"

class ApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_keys", verbose_name="Пользователь")
    key = models.CharField(max_length=255, unique=True, verbose_name="API ключ")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "API ключ"
        verbose_name_plural = "API ключи"

    def __str__(self):
        return f"API ключ для {self.user.username}"

