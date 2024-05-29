from rest_framework import generics
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response

from game.models import Game
from game.serializers import GameSerializer


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


class ListGameView(generics.ListAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        return Game.objects.filter(visible=True, is_archived=False)
