# Generated by Django 5.0.1 on 2024-06-19 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_working_partner_button'),
    ]

    operations = [
        migrations.AddField(
            model_name='working',
            name='partner_comment',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]