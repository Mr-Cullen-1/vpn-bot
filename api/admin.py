from django.contrib import admin
from .models import ApiKey, ApiLog
# Register your models here.

admin.site.register(ApiKey)
admin.site.register(ApiLog)