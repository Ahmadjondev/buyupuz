# Generated by Django 5.0.1 on 2024-02-25 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_remove_order_order_order_cash_order_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=16),
        ),
    ]