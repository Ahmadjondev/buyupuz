from decimal import Decimal
from datetime import datetime
import jwt
from django.forms import model_to_dict
from rest_framework import generics
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from user.models import User, BlacklistedToken
from user.serializers import UserSerializer
from .models import Carousel, Redeem, Notification, Working, PaymentCard
from .serializers import CarouselSerializer, RedeemSerializer, NotificationSerializer, RestTimeSerializer, \
    PaymentCardSerializer


class CarouselListView(generics.ListAPIView):
    queryset = Carousel.objects.all()
    serializer_class = CarouselSerializer


class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all().order_by('-id')
    serializer_class = NotificationSerializer


class RedeemCheckView(APIView):
    def post(self, request):
        token = request.headers['Authorization']
        user_id = checkToken(token)
        if user_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        redeem_code = request.data['code']
        try:
            red = Redeem.objects.get(code=redeem_code)
        except Redeem.DoesNotExist:
            return Response({"detail": "Promokod mavjud emas"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=user_id)
        json_user = dict(model_to_dict(user))
        json_redeem = dict(model_to_dict(red))

        if json_redeem['status']:
            return Response({'detail': "Promokod ishlatilgan!"}, status=status.HTTP_400_BAD_REQUEST)
        if status:
            balance_sum = float(json_user['balance'])
            balance_sum += float(json_redeem['price'])
            json_user['balance'] = Decimal("{:.2f}".format(balance_sum))
            json_redeem['status'] = True
            json_redeem['user'] = user_id
        serializer_user = UserSerializer(user, data=json_user)
        serializer_user.is_valid(raise_exception=True)
        serializer_user.save()
        serializer_red = RedeemSerializer(red, data=json_redeem)
        serializer_red.is_valid(raise_exception=True)
        serializer_red.save()
        return Response(
            {'message': f"{json_redeem['price']} so'm balansingizga qo'shildi", 'price': json_redeem['price']},
            status=status.HTTP_200_OK)


class RestTimeView(APIView):
    def get(self, request):
        try:
            first = Working.objects.all().first()
            json = RestTimeSerializer(first).data
            current_time = datetime.now()
            current_str = f"{f'0{current_time.hour}' if current_time.hour < 10 else current_time.hour}:{f'0{current_time.minute}' if current_time.minute < 10 else current_time.minute}"
            status_time = True
            if ((current_str >= json['start_time'] or current_str <= json['end_time'])
                    and json['start_time'] > json['end_time']):
                status_time = False
            response_json = {
                'start': json['start_time'],
                'end': json['end_time'],
                'working': status_time,
                'status': json['status'],
                'comment': json['comment'],
                "is_payment": json['is_payment'],
                "is_technical": json['is_technical'],
                "is_partner": json['is_partner'],
                "partner_comment": json['partner_comment'],
                "partner_link": json['partner_link'],
                "partner_button": json['partner_button']
            }
            return Response(response_json)
        except:
            return Response({'detail': "Vaqt mavjud emas"}, status=status.HTTP_400_BAD_REQUEST)


class PaymentCardView(generics.ListAPIView):
    queryset = PaymentCard.objects.all().order_by('-id')
    serializer_class = PaymentCardSerializer


def checkToken(token):
    try:
        if BlacklistedToken.objects.filter(token=token).exists():
            return -1
        code = jwt.decode(token, 'secret', algorithms='HS256')
        return code['id']
    except:
        return -1
