from django.db import models

# Create your models here.

class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name='Telegram ID')
    username = models.CharField(max_length=150, null=True, blank=True, verbose_name='Имя пользователя')
    phone_number = models.CharField(max_length=15, null=True, blank=True, verbose_name='Номер телефона')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    subscription_end = models.DateField(null=True, blank=True, verbose_name='Дата окончания подписки')
    date_registered = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username or str(self.telegram_id)

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Пользователь")
    plan_type = models.CharField(max_length=100, choices=[('day', 'Дневной'), ('month', 'Месячный'), ('year', 'Годовой')], verbose_name="Тип подписки")
    start_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата начала")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата окончания")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user.username} - {self.plan_type}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions", verbose_name="Пользователь")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    payment_method = models.CharField(max_length=100, choices=[('robokassa', 'Робокасса'), ('crypto', 'Криптовалюта'), ('telegram_stars', 'Telegram Stars')], verbose_name="Метод оплаты")
    status = models.CharField(max_length=50, choices=[('success', 'Успешно'), ('failed', 'Неудача')], verbose_name="Статус транзакции")
    transaction_id = models.CharField(max_length=255, unique=True, verbose_name="ID транзакции")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

    def __str__(self):
        return f"Транзакция {self.transaction_id} для {self.user.username}"

class AdminLog(models.Model):
    action = models.CharField(max_length=255, verbose_name="Действие")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь")
    admin = models.CharField(max_length=150, verbose_name="Администратор")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время действия")

    class Meta:
        verbose_name = "Лог админа"
        verbose_name_plural = "Логи админов"

    def __str__(self):
        return f"{self.admin} - {self.action}"
