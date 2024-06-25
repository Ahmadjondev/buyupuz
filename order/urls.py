from rest_framework.urls import path
from .views import CreateOrderView, ListOrderView

urlpatterns = [
    path('orders/create', CreateOrderView.as_view()),
    path('orders', ListOrderView.as_view()),
]
