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
        extra_kwargs = {
            'event_at': {
                'help_text': 'ISO 8601 datetime format (e.g., 2024-01-15T14:30:00Z)'
            },
            'event_type': {
                'help_text': 'Type of game event (e.g., game_start, game_end, level_complete)'
            },
            'ip_address': {
                'help_text': 'Player IP address (IPv4 or IPv6)'
            },
            'mac_address': {
                'help_text': 'Player MAC address (e.g., AA:BB:CC:DD:EE:FF)'
            },
            'session_id': {
                'help_text': 'Unique session identifier'
            },
            'game_reference': {
                'help_text': 'Game instance reference'
            },
            'game_level': {
                'help_text': 'Current game level (integer)'
            },
            'game_mode': {
                'help_text': 'Game mode (e.g., classic, timed, multiplayer)'
            },
            'game_color': {
                'help_text': 'Primary game color theme'
            },
            'game_sequence': {
                'help_text': 'Array of game sequence colors (e.g., ["red", "blue", "green"])'
            },
            'game_player_input': {
                'help_text': 'Array of player input colors (e.g., ["red", "blue"])'
            },
            'retry_count': {
                'help_text': 'Number of retry attempts (default: 0)'
            },
            'error_messages': {
                'help_text': 'Array of error messages with timestamps'
            }
        }
