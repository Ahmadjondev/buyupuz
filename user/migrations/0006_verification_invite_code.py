# Generated by Django 5.0.1 on 2024-02-20 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_invite_cashback'),
    ]

    operations = [
        migrations.AddField(
            model_name='verification',
            name='invite_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]