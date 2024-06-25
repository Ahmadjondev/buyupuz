from rest_framework import serializers

from payment.models import Payment
from user.serializers import UserSerializer


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
