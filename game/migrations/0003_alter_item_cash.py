# Generated by Django 5.0.1 on 2024-01-18 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_rename_create_at_game_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='cash',
            field=models.CharField(max_length=100),
        ),
    ]
