# serializers.py
from rest_framework import serializers

from user.models import User
from user.serializers import UserSerializer
from .models import Game, Item


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

    def create(self, validated_data):
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
        instance.input_type = validated_data.get('input_type', instance.input_type)
        instance.visible = validated_data.get('visible', instance.visible)
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
        instance.save()
        return instance
