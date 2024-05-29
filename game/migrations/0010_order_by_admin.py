# Generated by Django 5.0.1 on 2024-03-24 17:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_remove_order_by_admin'),
        ('manager', '0002_remove_manager_games'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='by_admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders_by_admin', to='manager.manager'),
        ),
    ]