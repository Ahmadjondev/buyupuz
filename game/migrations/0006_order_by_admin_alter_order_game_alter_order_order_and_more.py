# Generated by Django 5.0.1 on 2024-02-11 10:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_game_is_archived_game_keyboard_type_game_visible_and_more'),
        ('user', '0003_payment_by_admin_payment_comment_alter_payment_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='by_admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders_by_admin', to='user.user'),
        ),
        migrations.AlterField(
            model_name='order',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.game'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.item'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders_by_user', to='user.user'),
        ),
    ]
