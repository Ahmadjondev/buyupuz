from django.db import models

from game.models import Game
from manager.models import Manager
from user.models import User


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders_by_user')
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=16, default=0.00)
    cash = models.CharField(max_length=20, default='0')
    comment = models.CharField(max_length=255, blank=True, null=True)
    game_number = models.CharField(max_length=255)
    status = models.SmallIntegerField(default=0)
    by_admin = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, related_name='orders_by_admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.game_number}"
