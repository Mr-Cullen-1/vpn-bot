from django.contrib import admin
from .models import User, Subscription, Transaction, AdminLog

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "username", "phone_number", "is_active", "subscription_end", "date_registered")
    list_filter = ("is_active",)
    search_fields = ("username", "telegram_id", "phone_number")

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan_type", "start_date", "end_date", "is_active")
    list_filter = ("plan_type", "is_active")
    search_fields = ("user__username", "user__telegram_id")

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "payment_method", "status", "transaction_id", "date_created")
    list_filter = ("payment_method", "status")
    search_fields = ("transaction_id", "user__username", "user__telegram_id")

@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ("action", "admin", "timestamp", "user")
    list_filter = ("admin",)
    search_fields = ("action", "admin")
