# Generated by Django 5.0.1 on 2024-06-24 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_remove_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='cashback',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
    ]