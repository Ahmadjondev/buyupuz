from datetime import datetime, timedelta
from decimal import Decimal
from django.forms import model_to_dict
import jwt
from django.db.models import Sum
from django.utils import timezone

from game.models import Order
from game.serializers import OrderSerializer, OrderListSerializer
from manager.models import Manager
from manager.serializers import ManagerSerializer
from tools.notifications import sendNotification
from tools.secure import checkAPI
from user.models import Payment, User, Invite
from user.serializers import PaymentSerializer, UserSerializer, PaymentCreateSerializer, \
    InviteSerializer
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView


# Check User's payment
class CheckPaymentView(APIView):
    def check_permissions(self, request):
        if checkAPI(self.request.headers):
            raise AuthenticationFailed(detail="Siz dasturdan tashqaridasiz")
        admin_id = checkToken(request.headers['Authorization'])
        if admin_id == -1:
            self.permission_denied(self.request)

    def post(self, request):
        pay_id = request.data['id']
        comment = request.data['comment']
        pay = float(request.data['pay'])
        payment = Payment.objects.get(id=pay_id)
        json = dict(model_to_dict(payment))

        # check payment status and return to admin if checked

        if int(json['status']) != 0:
            return Response({'detail': "To'lov allaqachon amalga oshirilgan"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=json['user'])
        json_user = dict(model_to_dict(user))
        if int(request.data['status']) == 1:  # 0 = waiting, 1 = success, 2 = failed
            balance_sum = float(json_user['balance'])
            balance_sum += pay
            json_user['balance'] = Decimal(balance_sum)
        serializer_user = UserSerializer(user, data=json_user)
        serializer_user.is_valid(raise_exception=True)
        serializer_user.save()
        json['status'] = int(request.data['status'])
        json['price'] = pay
        json['comment'] = comment
        json['by_admin'] = checkToken(request.headers['Authorization'])
        serializer_pay = PaymentCreateSerializer(payment, data=json)
        serializer_pay.is_valid(raise_exception=True)
        serializer_pay.save()
        try:
            if int(request.data['status']) == 1:
                sendNotification(serializer_user.data['notification_token'], "To'lov",
                                 f"To'lov muvaffaqiyatli amalga oshirildi")
            if int(request.data['status']) == 2:
                sendNotification(serializer_user.data['notification_token'], "To'lov",
                                 f"To'lov admin tomonidan rad etildi")
        except:
            pass
        return Response({'update': "Success"}, status=status.HTTP_200_OK)


# Check User's order
class CheckOrderView(APIView):
    def check_permissions(self, request):
        if checkAPI(self.request.headers):
            raise AuthenticationFailed(detail="Siz dasturdan tashqaridasiz")
        admin_id = checkToken(request.headers['Authorization'])
        if admin_id == -1:
            self.permission_denied(self.request)

    def post(self, request):
        order_id = request.data['id']
        order_status = request.data['status']
        order = Order.objects.get(id=order_id)
        order_json = dict(model_to_dict(order))
        if int(order_json['status']) != 0:
            return Response({'detail': "Buyurtma allaqachon amalga oshirilgan"}, status=status.HTTP_400_BAD_REQUEST)
        admin_id = checkToken(request.headers['Authorization'])
        order_json['status'] = order_status
        order_json['by_admin'] = admin_id
        print(order_json)
        serializer_order = OrderSerializer(order, data=order_json)
        serializer_order.is_valid(raise_exception=True)
        serializer_order.save()
        user_json = dict(model_to_dict(User.objects.get(id=serializer_order.data['user'])))
        message = ""

        if order_status == 1:
            message = "Buyurtma bajrarildi!"
            if user_json['invite_code'] is not None:
                invite = Invite.objects.filter(code=user_json['invite_code']).first()
                if invite:
                    invite_serializer = dict(InviteSerializer(invite).data)
                    cashback = float(invite_serializer['cashback'])
                    price_mod = float(order_json['price']) * 0.003
                    cashback += price_mod
                    invite_serializer['cashback'] = f'{cashback}'
                    update_invite = InviteSerializer(invite, data=invite_serializer)
                    if update_invite.is_valid():
                        update_invite.save()
                self_invite = Invite.objects.filter(user=int(user_json['id'])).first()
                if self_invite:
                    invite_serializer = dict(InviteSerializer(self_invite).data)
                    cashback = float(invite_serializer['cashback'])
                    price_mod = float(order_json['price']) * 0.002
                    cashback += price_mod
                    invite_serializer['cashback'] = f'{cashback}'
                    update_invite = InviteSerializer(self_invite, data=invite_serializer)
                    if update_invite.is_valid():
                        update_invite.save()
            sendNotification(user_json['notification_token'], 'Buyurtma',
                             f"#{10000 + serializer_order.data['id']} raqamli buyurtma muvaffaqiyatli amalga oshirildi")
        if order_status == 2:
            message = "Buyurtmada xatolik"
            user = User.objects.get(id=order_json['user'])
            json_user = dict(model_to_dict(user))
            balance_sum = float(json_user['balance'])
            balance_sum += float(order_json['price'])
            json_user['balance'] = float(balance_sum)
            serializer_user = UserSerializer(user, data=json_user)
            serializer_user.is_valid(raise_exception=True)
            serializer_user.save()
            sendNotification(user_json['notification_token'], 'Buyurtma',
                             f"#{10000 + serializer_order.data['id']} raqamli buyurtma admin tomonidan rad etildi")
        return Response({'detail': message})


# All Payments
class PaymentListView(ListAPIView):
    serializer_class = PaymentSerializer

    def check_permissions(self, request):
        if checkAPI(self.request.headers):
            raise AuthenticationFailed(detail="Siz dasturdan tashqaridasiz")
        admin_id = checkToken(request.headers['Authorization'])
        if admin_id == -1:
            self.permission_denied(self.request)

    def get_queryset(self):
        today = timezone.now() 
        current_month_start = today - timedelta(days=2)
        queryset = Payment.objects.filter(created_at__range=(current_month_start, today)).order_by(
            '-created_at')
        return queryset

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     today = timezone.now()
    #     # month income
    #     current_month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    #     current_month_end = (current_month_start + timezone.timedelta(days=32)).replace(day=1, microsecond=0)
    #     month_pay = Payment.objects.filter(created_at__range=(current_month_start, current_month_end))
    #     # today income
    #     today_date_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
    #     today_date_end = today.replace(hour=23, minute=59, second=59, microsecond=59)
    #     today_pay = Payment.objects.filter(created_at__range=(today_date_start, today_date_end))
    #     today_income = today_pay.aggregate(Sum('price'))['price__sum'] or 0
    #     today_income_count = today_pay.count()
    #
    #     total_income = month_pay.aggregate(Sum('price'))['price__sum'] or 0
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #     response_data = {
    #         'month_income': total_income,
    #         'today_income': today_income,
    #         'today_income_count': today_income_count,
    #         'payments': serializer.data
    #     }
    #     return Response(response_data)


# All Orders
class OrderListView(ListAPIView):
    serializer_class = OrderListSerializer

    def check_permissions(self, request):
        if checkAPI(self.request.headers):
            raise AuthenticationFailed(detail="Siz dasturdan tashqaridasiz")
        admin_id = checkToken(request.headers['Authorization'])
        if admin_id == -1:
            self.permission_denied(self.request)

    def get_queryset(self):
        today = timezone.now()
        current_month_start = today - timedelta(days=2)
        queryset = Order.objects.filter(created_at__range=(current_month_start, today), ).order_by(
            '-created_at')
        return queryset


# Login for Admin
class Login(APIView):
    def check_permissions(self, request):
        if checkAPI(self.request.headers):
            raise AuthenticationFailed(detail="Siz dasturdan tashqaridasiz")

    def post(self, request):
        name = request.data['name']
        password = request.data['password']
        user = Manager.objects.filter(name=name).first()
        if user is None:
            raise AuthenticationFailed("Admin mavjud emas")
        user_json = dict(model_to_dict(user))
        if password != user.password:
            raise AuthenticationFailed("Parol xato kiritilgan")
        user_json['notification_token'] = request.data['notification_token']
        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(days=90),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, 'manager_secret_key', algorithm='HS256')
        response = Response()
        user_json['sign_count'] = int(user_json['sign_count']) + 1
        response.set_cookie(key='jwt', value=token, httponly=True)
        serializer = ManagerSerializer(user, data=user_json)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = dict(serializer.data)
        response_data['token'] = token
        response.data = response_data
        return response


class GetAdmin(APIView):
    def check_permissions(self, request):
        if checkAPI(self.request.headers):
            raise AuthenticationFailed(detail="Siz dasturdan tashqaridasiz")

    def get(self, request):
        token = self.request.headers['Authorization']
        admin_id = checkToken(token)
        if admin_id == -1:
            return Response({'detail': "Admin eskirgan"}, status=status.HTTP_400_BAD_REQUEST)
        man = Manager.objects.filter(id=int(admin_id)).first()
        if man:
            return Response(ManagerSerializer(man).data)
        else:
            return Response({'detail': "Admin mavjud emas"}, status=status.HTTP_401_UNAUTHORIZED)


class Statics(APIView):
    def check_permissions(self, request):
        if checkAPI(self.request.headers):
            raise AuthenticationFailed(detail="Siz dasturdan tashqaridasiz")
        admin_id = checkToken(request.headers['Authorization'])
        if admin_id == -1:
            self.permission_denied(self.request)

    def get(self, request):
        try:
            today = timezone.now() + timedelta(hours=5)
            # month income
            current_month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            current_month_end = (current_month_start + timezone.timedelta(days=32)).replace(day=1, microsecond=0)
            month_pay = Order.objects.filter(created_at__range=(current_month_start, current_month_end))
            total_income = month_pay.filter(status=1).aggregate(Sum('price'))['price__sum'] or 0
            waiting_income = month_pay.filter(status=0).aggregate(Sum('price'))['price__sum'] or 0
            total_count = month_pay.count()

            # today orders income
            today_date_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
            today_date_end = today.replace(hour=23, minute=59, second=59, microsecond=59)
            today_pay = month_pay.filter(created_at__range=(today_date_start, today_date_end))
            today_amount = today_pay.filter(status=1).aggregate(Sum('price'))['price__sum'] or 0
            today_waiting_amount = today_pay.filter(status=0).aggregate(Sum('price'))['price__sum'] or 0
            today_count = today_pay.count()

            waiting = month_pay.filter(status=0).count()
            success = month_pay.filter(status=1).count()
            reject = month_pay.filter(status=2).count()
            response_data = {
                'month': {
                    'amount': total_income,
                    'waiting_amount': waiting_income,
                    'count': total_count,
                },
                'today': {
                    'amount': today_amount,
                    'waiting_amount': today_waiting_amount,
                    'count': today_count,
                },
                'status': {
                    'waiting': waiting,
                    'success': success,
                    'reject': reject,
                },
            }
            return Response(response_data)
        except:

            return Response({'detail': "Xatolik"}, status=status.HTTP_400_BAD_REQUEST)


class UsersBalance(APIView):
    def get(self, request):
        total_balance = User.objects.filter(role=0).aggregate(Sum('balance'))['balance__sum'] or 0
        return Response({'total': total_balance})


def checkToken(token):
    code = jwt.decode(token, 'manager_secret_key', algorithms='HS256')
    return int(code['id'])
