from django.urls import path
from front.views import delete_account

urlpatterns = [
    path('delete-account', delete_account, name="Accountni o'chirish")
]
