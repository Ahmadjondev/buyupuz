from rest_framework.urls import path
from .views import ListGameView, ListItemView

urlpatterns = [
    path('games', ListGameView.as_view()),
    path('items', ListItemView.as_view()),
]
