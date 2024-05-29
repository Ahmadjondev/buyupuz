import jwt
from django.forms import model_to_dict
from rest_framework import generics, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tools.notifications import sendNotification
from tools.secure import checkAPI
from user.models import User, BlacklistedToken
from user.serializers import UserSerializer
from .models import Game, Item, Order
from .serializers import GameSerializer, ItemSerializer, OrderSerializer, OrderListSerializer


class ListGameView(generics.ListAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        return Game.objects.filter(visible=True, is_archived=False).order_by('id')


class ListItemView(generics.ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        game_id = self.request.query_params.get('game_id')
        if game_id:
            return Item.objects.filter(game=game_id, visible=True, is_archived=False).order_by('price')
        raise NotAuthenticated("Xatolik")


class CreateOrderView(APIView):
    def post(self, request):
        if checkAPI(self.request.headers):
            return Response({'detail': "Siz dasturdan tashqaridasiz"}, status=status.HTTP_400_BAD_REQUEST)
        token = request.headers['Authorization']
        user_id = checkToken(token)
        if user_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        json = dict(request.data)
        json['user'] = user_id
        user = User.objects.get(id=user_id)
        json_user = dict(model_to_dict(user))
        if float(json_user['balance']) < float(json['price']):
            return Response({'detail': "Balansdagi pul yetarli emas"}, status=status.HTTP_400_BAD_REQUEST)
        json_user['balance'] = float(json_user['balance']) - float(json['price'])
        serializer_user = UserSerializer(user, data=json_user)
        serializer_user.is_valid()
        serializer_user.save()
        serializer = OrderSerializer(data=json)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            sendNotification("/topics/admin", f"Buyurtma #{10000 + serializer.data['id']}",
                             f"Narxi: {json['price']}, Donat: {json['cash']}", serializer.data)
        except:
            pass
        return Response(serializer.data)


def checkToken(token):
    try:
        if BlacklistedToken.objects.filter(token=token).exists():
            return -1
        code = jwt.decode(token, 'secret', algorithms='HS256')
        return code['id']
    except:
        return -1


class ListOrderView(generics.ListAPIView):
    serializer_class = OrderListSerializer

    def get_queryset(self):
        token = self.request.headers['Authorization']
        user_id = checkToken(token)
        if user_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        return Order.objects.filter(user=user_id).order_by('-id')