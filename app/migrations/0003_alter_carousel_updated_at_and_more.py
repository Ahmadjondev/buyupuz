# Generated by Django 5.0.1 on 2024-01-19 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_create_at_carousel_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carousel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='redeem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
