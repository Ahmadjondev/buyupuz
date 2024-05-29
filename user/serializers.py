import random

from django.utils import timezone
from rest_framework import serializers
from .models import User, Payment, Verification, Invite, CashbackOrder
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.password = make_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.balance = validated_data.get('balance', instance.balance)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.name = validated_data.get('name', instance.name)
        instance.invite_code = validated_data.get('invite_code', instance.invite_code)
        instance.spam = validated_data.get('spam', instance.spam)
        instance.is_google = validated_data.get('is_google', instance.is_google)
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        instance.notification_token = validated_data.get('notification_token', instance.notification_token)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.name = validated_data.get('name', instance.name)
        instance.spam = validated_data.get('spam', instance.spam)
        instance.is_google = validated_data.get('is_google', instance.is_google)
        instance.save()
        return instance


class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = '__all__'
        extra_kwargs = {
            'verify_code': {'read_only': True}
        }

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.verify_code = random.randint(1000, 9999)
        instance.save()
        return instance


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        instance.status = validated_data.get('status', instance.status)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.screenshot = validated_data.get('screenshot', instance.screenshot)
        instance.by_admin = validated_data.get('by_admin', instance.by_admin)
        instance.save()
        return instance


class InviteSerializer(serializers.ModelSerializer):
    statics = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Invite
        fields = ('id', 'user', 'cashback', 'code', 'statics')

    def update(self, instance, validated_data):
        instance.cashback = validated_data.get('cashback', instance.cashback)
        instance.save()
        return instance

    def get_statics(self, obj):
        users = User.objects.filter(invite_code=obj.code)
        total = users.count()
        today = timezone.now()
        today_date_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        today_date_end = today.replace(hour=23, minute=59, second=59, microsecond=59)
        today_users = users.filter(created_at__range=(today_date_start, today_date_end)).count()
        return {
            'total': int(total),
            'today': int(today_users)
        }


class CashbackOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashbackOrder
        fields = '__all__'
