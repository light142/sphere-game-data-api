from django.db import models
from django.contrib.auth.models import User


class GameData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    event_at = models.DateTimeField(db_index=True)  # Index for time-based queries
    event_type = models.CharField(max_length=255, db_index=True)  # Index for event type filtering
    event_category = models.CharField(max_length=255, default="general", blank=False, db_index=True)  # Index for category filtering
    ip_address = models.GenericIPAddressField(db_index=True)  # Index for IP-based queries
    mac_address = models.CharField(max_length=17, default="00:00:00:00:00:00")  # MAC address format: XX:XX:XX:XX:XX:XX
    session_id = models.CharField(max_length=255, db_index=True)  # Index for session tracking
    game_reference = models.CharField(max_length=255, blank=True, default="")
    game_level = models.IntegerField(db_index=True)  # Index for level-based analytics
    game_mode = models.CharField(max_length=255, db_index=True)  # Index for mode filtering
    game_color = models.CharField(max_length=255, blank=True, default="")
    correct_game_color = models.CharField(max_length=255, blank=True, default="")  # The correct color for this event
    game_sequence = models.JSONField(default=list)
    game_player_input = models.JSONField(default=list)
    retry_count = models.IntegerField(default=0)
    error_messages = models.JSONField(default=list)

    class Meta:
        indexes = [
            # Composite indexes for common query patterns
            models.Index(fields=['session_id', 'event_at'], name='gd_session_time_idx'),
            models.Index(fields=['event_type', 'event_category'], name='gd_type_cat_idx'),
            models.Index(fields=['event_at', 'event_type'], name='gd_time_type_idx'),
            models.Index(fields=['ip_address', 'event_at'], name='gd_ip_time_idx'),
        ]
