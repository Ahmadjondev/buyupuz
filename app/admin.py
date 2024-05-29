from django.contrib import admin
from .models import Notification, Carousel, Redeem, Working, PaymentCard


@admin.register(Notification)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')
    search_fields = ('name', 'description')


@admin.register(Carousel)
class CarouselsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'url', 'link')
    search_fields = ('name', 'description')


@admin.register(Redeem)
class RedeemAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'price', 'status')


@admin.register(Working)
class RestTimeAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time')


@admin.register(PaymentCard)
class PaymentCardAdmin(admin.ModelAdmin):
    list_display = ('name', 'card', 'type')
