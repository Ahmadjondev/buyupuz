from django.db import models

from manager.models import Manager


class User(models.Model):
    name = models.CharField(max_length=55, null=False, blank=True)
    email = models.CharField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.SmallIntegerField(default=0)
    balance = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    notification_token = models.CharField(max_length=1001, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    spam = models.IntegerField(default=0)
    is_google = models.BooleanField(default=False)
    invite_code = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Verification(models.Model):
    name = models.CharField(max_length=55, null=False, blank=True)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=55)
    notification_token = models.CharField(max_length=1001, null=True, blank=True)
    verify_code = models.CharField(max_length=6)
    invite_code = models.CharField(max_length=10, null=True, blank=True)
    expired_date = models.SmallIntegerField(default=180)

    def __str__(self):
        return self.name


# class PaymentOld(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
#     price = models.DecimalField(max_digits=16, decimal_places=2)
#     status = models.SmallIntegerField(default=0)
#     type = models.SmallIntegerField(default=0)
#     screenshot = models.ImageField(upload_to='payment_screenshots/')
#     comment = models.CharField(max_length=500, null=True, blank=True)
#     by_admin = models.ForeignKey(Manager, null=True, on_delete=models.SET_NULL)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.user.name
#

class Invite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, unique=True)
    cashback = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)


class CashbackOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_card = models.CharField(max_length=16, null=False)
    amount = models.DecimalField(decimal_places=2, max_digits=16, null=False, default='0.00')
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=1000, unique=True)

    def __str__(self):
        return self.token
