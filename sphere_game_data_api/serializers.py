from rest_framework import serializers
from django.contrib.auth.models import User

from sphere_game_data_api.models import GameData


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(username=data["username"]).first()
        if not user:
            raise serializers.ValidationError("User not found")
        return data


class LogoutSerializer(serializers.Serializer):
    pass


class GameDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameData
        fields = [
            "id", 
            "created_at", 
            "event_at", 
            "event_type", 
            "ip_address", 
            "mac_address", 
            "session_id", 
            "game_reference", 
            "game_level", 
            "game_mode", 
            "game_color", 
            "game_sequence", 
            "game_player_input",
            "retry_count",
            "error_messages"
        ]
