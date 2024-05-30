from django.forms import model_to_dict
from rest_framework import generics, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import Order
from order.serializers import OrderListSerializer, OrderSerializer
from tools.generate_token import checkToken
from tools.notifications import sendNotification
from tools.secure import checkAPI
from user.models import User
from user.serializers import UserSerializer


# Create your views here.


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


class ListOrderView(generics.ListAPIView):
    serializer_class = OrderListSerializer

    def get_queryset(self):
        token = self.request.headers['Authorization']
        user_id = checkToken(token)
        if user_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        return Order.objects.filter(user=user_id).order_by('-id')
