# Generated by Django 5.0.1 on 2024-06-19 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_working_is_payment_working_is_technical'),
    ]

    operations = [
        migrations.AddField(
            model_name='working',
            name='is_partner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='working',
            name='partner_link',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
