from django.contrib import admin
from game.models import Game, Order, Item


# Register your models here.
@admin.register(Game)
class GamesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'currency')


@admin.register(Item)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'price', 'cash', 'bonus', 'created_at')


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'user', 'cash', 'price', 'game_number','status','created_at')
    search_fields = ('id','user__name', 'cash', 'price', 'game_number','created_at')
