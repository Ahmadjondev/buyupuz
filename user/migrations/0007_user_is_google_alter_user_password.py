# Generated by Django 5.0.1 on 2024-03-02 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_verification_invite_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_google',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]