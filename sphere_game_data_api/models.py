from django.db import models
from django.contrib.auth.models import User


class GameData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event_at = models.DateTimeField()
    event_type = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=17, default="00:00:00:00:00:00")  # MAC address format: XX:XX:XX:XX:XX:XX
    session_id = models.CharField(max_length=255)
    game_reference = models.CharField(max_length=255)
    game_level = models.IntegerField()
    game_mode = models.CharField(max_length=255)
    game_color = models.CharField(max_length=255)
    game_sequence = models.JSONField(default=list)
    game_player_input = models.JSONField(default=list)
