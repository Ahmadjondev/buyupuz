from django.contrib import admin

from manager.models import Manager


# Register your models here.

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'sign_count')

    # search_fields = ('username',)
