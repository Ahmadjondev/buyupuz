# Generated by Django 5.0.1 on 2024-03-24 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manager',
            name='games',
        ),
    ]
