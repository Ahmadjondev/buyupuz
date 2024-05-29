# Generated by Django 4.2.11 on 2024-04-23 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_working_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentcard',
            name='type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='paymentcard',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='payment_card/'),
        ),
    ]