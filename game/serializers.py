# serializers.py
from rest_framework import serializers

from user.models import User
from user.serializers import UserSerializer
from .models import Game, Item, Order


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        json = dict(validated_data)
        json['visible'] = True
        instance = self.Meta.model(**json)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.keyboard_type = validated_data.get('keyboard_type', instance.keyboard_type)
        instance.visible = validated_data.get('visible', instance.visible)
        instance.is_archived = validated_data.get('is_archived', instance.is_archived)
        instance.save()
        return instance


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.cash = validated_data.get('cash', instance.cash)
        instance.bonus = validated_data.get('bonus', instance.bonus)
        instance.price = validated_data.get('price', instance.price)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.visible = validated_data.get('visible', instance.visible)
        instance.is_archived = validated_data.get('is_archived', instance.is_archived)
        instance.save()
        return instance


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
