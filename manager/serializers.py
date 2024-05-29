from rest_framework import serializers

from game.serializers import GameSerializer
from manager.models import Manager


class ManagerSerializer(serializers.ModelSerializer):
    games = GameSerializer(many=True, read_only=True)

    class Meta:
        model = Manager
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            # 'games': {'read_only': True}
        }
