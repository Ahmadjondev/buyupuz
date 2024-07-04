from decimal import Decimal
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, APIException
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from manager.models import Manager
from payment.models import Payment
from payment.serializers import PaymentSerializer, PaymentCreateSerializer
from tools.generate_token import checkToken
from tools.notifications import send_notification_v2
from tools.secure import checkAPI
from user.models import User
from user.serializers import UserSerializer


class PaymentView(ListAPIView):
    serializer_class = PaymentSerializer
    
    def check_permissions(self, request):
        if checkAPI(self.request.headers):
            raise APIException({'detail': "Siz dasturdan tashqaridasiz"})

    def get_queryset(self):
        token = self.request.headers['Authorization']
        user_id = checkToken(token)
        if user_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        payments = Payment.objects.filter(user_id=user_id).order_by('-id')

        return payments

    def post(self, request):
        token = request.headers['Authorization']
        user_id = checkToken(token)
        if user_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        datas = {'price': self.request.data['price'],
                 'screenshot': self.request.data['screenshot'],
                 'user': user_id}
        serializer = PaymentCreateSerializer(data=datas)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            managers = Manager.objects.filter(is_staff=True).values()
            for man in managers:
                fcm_token = man['notification_token']
                send_notification_v2(token=fcm_token, title=f"To`lov qilindi",
                                 msg=f"Foydalanuvchi to`lov qildi [{self.request.data['price']} so'm]", data=serializer.data,
                                 is_order_or_payment=True)
        except:
            pass
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ApplePayView(APIView):
    def post(self,request):
        try:
            pay = float(request.data['pay'])
            token = self.request.headers['Authorization']
            user_id = checkToken(token)
            if user_id == -1:
                raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
            user = User.objects.get(id=user_id)
            if user.spam > 2:
                return Response({"detail" : "Foydalanuvchi blocklangan"}, status=status.HTTP_400_BAD_REQUEST)
            json_user = dict(model_to_dict(user))
            balance_sum = float(json_user['balance'])
            balance_sum += pay
            json_user['balance'] = Decimal(balance_sum)
            serializer_user = UserSerializer(user, data=json_user)
            serializer_user.is_valid(raise_exception=True)
            serializer_user.save()
        except:
            return Response({"detail" : "Xatolik"}, status=status.HTTP_400_BAD_REQUEST)
