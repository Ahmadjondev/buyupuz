from django.db import models

from manager.models import Manager
from user.models import User


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    price = models.DecimalField(max_digits=16, decimal_places=2)
    status = models.SmallIntegerField(default=0)
    type = models.SmallIntegerField(default=0)
    screenshot = models.ImageField(upload_to='payment_screenshots/')
    comment = models.CharField(max_length=500, null=True, blank=True)
    by_admin = models.ForeignKey(Manager, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name
