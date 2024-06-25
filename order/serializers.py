# serializers.py
from rest_framework import serializers

from game.serializers import GameSerializer
from user.serializers import UserSerializer
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # print(validated_data)
        instance.status = validated_data.get('status', instance.status)
        instance.by_admin = validated_data.get('by_admin', instance.by_admin)
        instance.save()
        return instance


class OrderListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    game = GameSerializer()

    class Meta:
        model = Order
        fields = '__all__'
