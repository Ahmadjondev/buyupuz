from django.contrib import admin

from order.models import Order


# Register your models here.


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'user', 'cash', 'price', 'game_number','status','created_at')
    search_fields = ('id','user__name', 'cash', 'price', 'game_number','created_at')
