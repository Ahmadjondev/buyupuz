from django.db import models

from user.models import User


class Notification(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='notifications_images/', null=True)
    url = models.CharField(max_length=200, null=True)
    link = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Carousel(models.Model):
    image = models.ImageField(upload_to='carousels_images/')
    title = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=1000, null=True)
    url = models.CharField(max_length=200, null=True)
    link = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Redeem(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code}: {self.price} so'm"


class Working(models.Model):
    start_time = models.CharField(max_length=30, null=True)  # 12:00
    end_time = models.CharField(max_length=30, null=True)  # 07:00
    status = models.BooleanField(null=True)
    comment = models.CharField(max_length=255, null=True)
    is_payment = models.BooleanField(default=False)
    is_technical = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    partner_comment = models.CharField(max_length=300, null=True, blank=True)
    partner_link = models.CharField(max_length=255, null=True, blank=True)
    partner_button = models.CharField(max_length=55, null=True, blank=True)

    def __str__(self):
        return f"{self.start_time}: {self.end_time}"


class Currency(models.Model):
    country = models.CharField(max_length=55)
    code = models.CharField(max_length=10)
    rate = models.DecimalField(decimal_places=2, max_digits=16)


class PaymentCard(models.Model):
    name = models.CharField(max_length=100, default='')
    card = models.CharField(max_length=20)
    type = models.CharField(max_length=20, blank=True, null=True)
    icon = models.ImageField(upload_to='payment_card/', null=True, blank=True)
