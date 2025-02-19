# Generated by Django 5.1.5 on 2025-01-22 08:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bot_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, unique=True, verbose_name='API ключ')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_keys', to='bot_management.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'API ключ',
                'verbose_name_plural': 'API ключи',
            },
        ),
        migrations.CreateModel(
            name='ApiLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255, verbose_name='Действие')),
                ('request_payload', models.TextField(verbose_name='Параметры запроса')),
                ('response_payload', models.TextField(verbose_name='Ответ сервера')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Время запроса')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='api_logs', to='bot_management.user', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Лог API',
                'verbose_name_plural': 'Логи API',
            },
        ),
    ]
