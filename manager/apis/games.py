from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response

from game.models import Game
from game.serializers import GameSerializer
from manager.models import Manager
from tools.generate_token import check_token_manager


class GamesAdminView(generics.ListAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        token_admin = self.request.headers['Authorization']
        admin_id = check_token_manager(token_admin)
        print(admin_id)
        if admin_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        manager = model_to_dict(Manager.objects.get(id=admin_id))
        if manager['is_superadmin']:
            return Game.objects.all()
        games = Game.objects.filter(manager=admin_id)
        print(games)
        return games


class GameUpdateView(generics.UpdateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CreateGameView(CreateAPIView):
    serializer_class = GameSerializer


class GameDeleteView(DestroyAPIView):
    serializer_class = GameSerializer
    queryset = Game.objects.all()

    def perform_destroy(self, instance):
        instance.delete()
