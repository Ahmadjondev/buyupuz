from django.contrib import admin

from payment.models import Payment


# Register your models here.


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'price', 'created_at', 'status')
    search_fields = ('user__name', 'price', 'created_at', 'status')
