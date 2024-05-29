from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Carousel, Redeem, Notification, Working, PaymentCard


class CarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = ['id', 'image', 'title', 'description', 'url', 'link']


class RedeemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Redeem
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance


class RedeemListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Redeem
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'image', 'url', 'link', 'created_at']


class RestTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Working
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.status = validated_data.get('status', instance.status)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance


class PaymentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCard
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.card = validated_data.get('card', instance.card)
        instance.name = validated_data.get('name', instance.name)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.save()
        return instance
