import string
import random

from datetime import datetime, timedelta

import jwt
from django.contrib.auth.hashers import check_password
from django.forms import model_to_dict
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, ParseError
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from tools.generate_token import generate_token_jwt, checkToken
from tools.secure import checkAPI

from user.models import User, BlacklistedToken, Verification, Invite, CashbackOrder
from user.serializers import UserSerializer, UserUpdateSerializer, \
    VerifySerializer, InviteSerializer, CashbackOrderSerializer
from django.core.mail import send_mail


class Register(APIView):
    def post(self, request):
        if checkAPI(self.request.headers):
            return Response({'detail': "Siz dasturdan tashqaridasiz"}, status=status.HTTP_400_BAD_REQUEST)
        email_str = request.data['email']
        check_email = User.objects.filter(email=email_str).first()
        if check_email:
            return Response({'detail': 'Bunday email mavjud'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        subject = "Emailni tasdiqlash"
        message = render_to_string('email_verification.html', {'user': serializer.data['name'],
                                                               'code': serializer.data['verify_code']})
        plain_message = strip_tags(message)
        send_mail(subject, plain_message, "<no-reply@buyup.uz>", [serializer.data['email']], html_message=message)
        return Response({'message': "Tasdiqlash uchun kod emailingizga yuborildi."}, status=status.HTTP_200_OK)


class GoogleSign(APIView):
    def post(self, request):
        data = request.data
        name = data['name']
        email = data['email']
        notification_token = data['notification_token']
        check_email = User.objects.filter(email=email).first()
        if check_email:
            user_serializer = UserUpdateSerializer(check_email, data={
                'name': name,
                'email': email,
                'notification_token': notification_token
            })

            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            log_user = dict(user_serializer.data)
            gen_token = generate_token_jwt(log_user['id'])
            log_user['token'] = gen_token
            return Response(log_user, status=status.HTTP_200_OK)

        serializer = UserSerializer(data={
            'name': name,
            'email': email,
            'notification_token': notification_token,
            'is_google': True
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_json = dict(serializer.data)
        user_json['token'] = generate_token_jwt(serializer.data['id'])
        return Response(user_json, status=status.HTTP_200_OK)


class ResendCodeView(APIView):
    def post(self, request):
        if checkAPI(self.request.headers):
            return Response({'detail': "Siz dasturdan tashqaridasiz"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        subject = "Emailni tasdiqlash"
        message = render_to_string('email_verification.html', {'user': serializer.data['name'],
                                                               'code': serializer.data['verify_code']})
        plain_message = strip_tags(message)
        send_mail(subject, plain_message, 'noreply@buyup.uz', [serializer.data['email']], html_message=message)
        return Response({'message': "Tasdiqlash uchun kod emailingizga yuborildi."}, status=status.HTTP_200_OK)


class VerifyView(APIView):
    def post(self, request):
        if checkAPI(self.request.headers):
            return Response({'detail': "Siz dasturdan tashqaridasiz"}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data['email']
        code = request.data['code']
        verify = Verification.objects.filter(email=email, verify_code=code).first()
        if verify is None:
            return Response({'detail': "Kod xato"}, status=status.HTTP_400_BAD_REQUEST)
        verify_json = dict(model_to_dict(verify))
        verify_json.pop('id')
        verify_json.pop('verify_code')
        verify_json.pop('expired_date')
        serializer = UserSerializer(data=verify_json)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_json = dict(serializer.data)
        payload = {
            'id': serializer.data['id'],
            'exp': datetime.utcnow() + timedelta(days=50),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        user_json['token'] = token
        verify.delete()
        return Response(user_json)


class Login(APIView):
    def post(self, request):
        if checkAPI(self.request.headers):
            return Response({'detail': "Siz dasturdan tashqaridasiz"}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User mavjud emas")

        if not check_password(password, user.password):
            raise AuthenticationFailed("Parol xato kiritilgan")
        user_json = dict(model_to_dict(user))
        user_json['notification_token'] = request.data['notification_token']
        user_json['is_google'] = False
        serializer_user = UserUpdateSerializer(user, data=user_json)
        serializer_user.is_valid(raise_exception=True)
        serializer_user.save()
        payload = {
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(days=50),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'token': token,
            'name': user.name,
            'email': user.email,
            'balance': user.balance,
            'avatar': user.avatar,
            'spam': user.spam
        }
        return response


class Logout(APIView):

    def post(self, request):
        if checkAPI(self.request.headers):
            return Response({'detail': "Siz dasturdan tashqaridasiz"}, status=status.HTTP_400_BAD_REQUEST)

        token = request.data.get('token')
        if not token:
            return Response({'detail': 'Token yuborilmagan'}, status=status.HTTP_400_BAD_REQUEST)

        if BlacklistedToken.objects.filter(token=token).exists():
            return Response({'detail': 'Token allaqachon o`chirilgan'}, status=status.HTTP_400_BAD_REQUEST)

        BlacklistedToken.objects.create(token=token)

        return Response({'detail': 'Muvaffaqiyatli chiqildi'}, status=status.HTTP_200_OK)


class GetUser(APIView):
    def get(self, request):
        if checkAPI(self.request.headers):
            return Response({'detail': "Siz dasturdan tashqaridasiz"}, status=status.HTTP_400_BAD_REQUEST)

        token = self.request.headers['Authorization']
        user_id = checkToken(token)
        if user_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except:
            return Response({'detail': "Foydalanuvchi mavjud emas"}, status=status.HTTP_401_UNAUTHORIZED)


class UpdateUserView(APIView):
    def put(self, request):
        if checkAPI(self.request.headers):
            return Response({'detail': "Siz dasturdan tashqaridasiz"}, status=status.HTTP_400_BAD_REQUEST)

        token = self.request.headers['Authorization']
        user_id = checkToken(token)
        if user_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        user = User.objects.get(id=user_id)
        json_user = model_to_dict(user)
        update_data = {
            'avatar': request.data['avatar'],
            'name': request.data['name'],
            'notification_token': request.data['notification_token'],
            'email': json_user['email'],
        }
        serializer = UserUpdateSerializer(user, data=update_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class InviteStatView(APIView):
    def get(self, request):
        if checkAPI(self.request.headers):
            return Response({'detail': "Siz dasturdan tashqaridasiz"}, status=status.HTTP_400_BAD_REQUEST)
        token = self.request.headers['Authorization']
        user_id = checkToken(token)
        if user_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        try:
            invite = Invite.objects.get(user=user_id)
            serializer = InviteSerializer(invite)
            return Response(serializer.data)
        except:
            return Response({'detail': "Yaratish"}, status=status.HTTP_400_BAD_REQUEST)


class InviteCreateView(APIView):

    def post(self, request):
        if checkAPI(self.request.headers):
            return Response({'detail': "Siz dasturdan tashqaridasiz"}, status=status.HTTP_400_BAD_REQUEST)
        token = self.request.headers['Authorization']
        user_id = checkToken(token)
        if user_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        check = Invite.objects.filter(user=user_id).first()
        if check:
            return Response({'detail': "Allaqachon yaratilgan"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            characters = string.ascii_uppercase + string.digits
            random_code = None
            while True:
                random_code = ''.join(random.choices(characters, k=6))
                first = Invite.objects.filter(code=random_code).first()
                if not first:
                    break

            data = {
                'user': user_id,
                'code': random_code,
                'cashback': 0.00
            }
            serializer = InviteSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except:
            return Response({'detail': "Malumot yo'q"}, status=status.HTTP_400_BAD_REQUEST)


class CashbackOrdersView(ListCreateAPIView):
    serializer_class = CashbackOrderSerializer

    def perform_create(self, serializer):
        token = self.request.headers['Authorization']
        user_id = checkToken(token)
        if user_id == -1:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        invite = Invite.objects.filter(user=user_id).first()
        invite_json = model_to_dict(invite)
        data = serializer.validated_data
        if float(data['amount']) > float(invite_json['cashback']):
            raise ParseError(detail="Cashback yetarli emas")
        invite_json['cashback'] = str(float(invite_json['cashback']) - float(data['amount']))
        invite_serializer = InviteSerializer(invite, data=invite_json)
        if not invite_serializer.is_valid():
            raise ParseError(detail="No'malum xatolik")
        invite_serializer.save()
        serializer.save(user=data['user'])

    def get_queryset(self):
        try:
            if checkAPI(self.request.headers):
                return Response({'detail': "Siz dasturdan tashqaridasiz"}, status=status.HTTP_400_BAD_REQUEST)
            token = self.request.headers['Authorization']
            user_id = checkToken(token)
            if user_id == -1:
                raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        except:
            raise NotAuthenticated(detail="Ro'yxatdan o'tilmagan")
        cashback = CashbackOrder.objects.filter(user=user_id).order_by('-id')
        return cashback
