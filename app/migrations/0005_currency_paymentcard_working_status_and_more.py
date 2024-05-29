# Generated by Django 5.0.1 on 2024-03-08 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_create_at_notification_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=55)),
                ('code', models.CharField(max_length=10)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=16)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('card', models.CharField(max_length=20)),
                ('icon', models.ImageField(null=True, upload_to='payment_card/')),
            ],
        ),
        migrations.AddField(
            model_name='working',
            name='status',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='working',
            name='end_time',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='working',
            name='start_time',
            field=models.CharField(max_length=30, null=True),
        ),
    ]