from rest_framework import generics
from rest_framework.exceptions import NotAuthenticated, APIException

from tools.secure import checkAPI
from .models import Game, Item
from rest_framework import status
from .serializers import GameSerializer, ItemSerializer


class ListGameView(generics.ListAPIView):
    serializer_class = GameSerializer
    def check_permissions(self, request):
        if checkAPI(self.request.headers):
            raise APIException({'detail': "Siz dasturdan tashqaridasiz"})

    def get_queryset(self):
        return Game.objects.filter(visible=True).order_by('id')


class ListItemView(generics.ListAPIView):
    serializer_class = ItemSerializer
    def check_permissions(self, request):
        if checkAPI(self.request.headers):
            raise APIException({'detail': "Siz dasturdan tashqaridasiz"})

    def get_queryset(self):
        game_id = self.request.query_params.get('game_id')
        if game_id:
            return Item.objects.filter(game=game_id, visible=True).order_by('price')
        raise NotAuthenticated("Xatolik")