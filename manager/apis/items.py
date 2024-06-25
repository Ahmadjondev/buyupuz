from rest_framework import generics
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response

from game.models import Item
from game.serializers import ItemSerializer


class ItemUpdateView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        print(request.data)
        print(serializer.data)
        return Response(serializer.data)


class ListItemView(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        game_id = self.request.query_params.get('game_id')
        if game_id:
            return Item.objects.filter(game=game_id).order_by('price')
        raise NotAuthenticated("Xatolik")


class CreateItemView(CreateAPIView):
    serializer_class = ItemSerializer


class ItemDeleteView(DestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def perform_destroy(self, instance):
        instance.delete()
