from django.db import models
from manager.models import Manager

from user.models import User


class Game(models.Model):
    KEYBOARD_CHOICES = [
        ('text', 'Text'),
        ('number', 'Number'),
    ]
    name = models.CharField(max_length=101)
    image = models.ImageField(upload_to='games_images/')
    currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    keyboard_type = models.CharField(max_length=20, choices=KEYBOARD_CHOICES, default='text')

    def __str__(self):
        return f"{self.name}"


class Item(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    cash = models.CharField(max_length=100)
    bonus = models.IntegerField(null=True, blank=True)
    discount = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.game}: {self.cash}"


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
