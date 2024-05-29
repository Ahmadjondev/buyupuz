from rest_framework.urls import path
from .views import  ListGameView, ListItemView, CreateOrderView,ListOrderView

urlpatterns = [   
    path('games', ListGameView.as_view()),
    path('items', ListItemView.as_view()),
    path('orders/create', CreateOrderView.as_view()),
    path('orders', ListOrderView.as_view()),
]
