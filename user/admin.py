from django.contrib import admin

from user.models import User, Verification, Invite, CashbackOrder


# Register your models here.
@admin.register(Verification)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'verify_code')
    search_fields = ('name', 'email')


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'balance', 'spam', 'created_at')
    search_fields = ('name', 'email')


# @admin.register(PaymentOld)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'price', 'created_at', 'status')
#     search_fields = ('user__name', 'price', 'created_at', 'status')


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code', 'cashback')


@admin.register(CashbackOrder)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'payment_card', 'status', 'created_at')
