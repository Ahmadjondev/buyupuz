from rest_framework import generics
from rest_framework.exceptions import NotAuthenticated
from .models import Game, Item
from .serializers import GameSerializer, ItemSerializer


class ListGameView(generics.ListAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        return Game.objects.filter(visible=True).order_by('id')


class ListItemView(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        game_id = self.request.query_params.get('game_id')
        if game_id:
            return Item.objects.filter(game=game_id, visible=True).order_by('price')
        raise NotAuthenticated("Xatolik")
