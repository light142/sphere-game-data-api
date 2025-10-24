# tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime
from django.utils import timezone
from sphere_game_data_api.models import GameData


class AuthAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    # Test User Login
    def test_login_user(self):
        url = reverse("login")
        data = {"username": self.user.username, "password": "testpass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    # Test Admin User Login
    def test_admin_login(self):
        # Create admin user if it doesn't exist
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={"password": "P@ssw0rd!123", "is_staff": True, "is_superuser": True}
        )
        if created:
            admin_user.set_password("P@ssw0rd!123")
            admin_user.save()
        
        url = reverse("login")
        data = {"username": "admin", "password": "P@ssw0rd!123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)


class GameDataAPITestCase(APITestCase):
    def setUp(self):
        # Create test game data
        self.game_data = GameData.objects.create(
            event_at=timezone.now(),
            event_type="game_start",
            ip_address="192.168.1.1",
            mac_address="AA:BB:CC:DD:EE:FF",
            session_id="test_session_123",
            game_reference="game_ref_001",
            game_level=1,
            game_mode="classic",
            game_color="blue",
            game_sequence=["red", "blue", "green"],
            game_player_input=["red", "blue"]
        )
        
        # Create admin user for admin-only tests
        self.admin_user = User.objects.create_user(
            username="admin_test",
            password="adminpass123",
            is_staff=True,
            is_superuser=True
        )
        self.admin_token = Token.objects.create(user=self.admin_user)

    def test_create_game_data_anonymous(self):
        """Test that anyone can create game data without authentication"""
        url = reverse("game-data-list-create")
        data = {
            "event_at": "2024-01-01T12:00:00Z",
            "event_type": "game_end",
            "ip_address": "192.168.1.2",
            "mac_address": "11:22:33:44:55:66",
            "session_id": "session_456",
            "game_reference": "game_ref_002",
            "game_level": 2,
            "game_mode": "timed",
            "game_color": "red",
            "game_sequence": ["blue", "red", "yellow"],
            "game_player_input": ["blue", "red"]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GameData.objects.count(), 2)

    def test_list_game_data_anonymous_denied(self):
        """Test that anonymous users cannot list game data"""
        url = reverse("game-data-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_game_data_admin_allowed(self):
        """Test that admin users can list game data"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        url = reverse("game-data-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_game_data_anonymous_denied(self):
        """Test that anonymous users cannot retrieve game data"""
        url = reverse("game-data-rud", kwargs={"pk": self.game_data.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_game_data_admin_allowed(self):
        """Test that admin users can retrieve game data"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        url = reverse("game-data-rud", kwargs={"pk": self.game_data.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["event_type"], "game_start")

    def test_update_game_data_anonymous_denied(self):
        """Test that anonymous users cannot update game data"""
        url = reverse("game-data-rud", kwargs={"pk": self.game_data.pk})
        data = {
            "event_at": "2024-01-01T12:00:00Z",
            "event_type": "game_pause",
            "ip_address": "192.168.1.1",
            "mac_address": "AA:BB:CC:DD:EE:FF",
            "session_id": "test_session_123",
            "game_reference": "game_ref_001",
            "game_level": 1,
            "game_mode": "classic",
            "game_color": "blue",
            "game_sequence": ["red", "blue", "green"],
            "game_player_input": ["red", "blue"]
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_game_data_admin_allowed(self):
        """Test that admin users can update game data"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        url = reverse("game-data-rud", kwargs={"pk": self.game_data.pk})
        data = {
            "event_at": "2024-01-01T12:00:00Z",
            "event_type": "game_pause",
            "ip_address": "192.168.1.1",
            "mac_address": "AA:BB:CC:DD:EE:FF",
            "session_id": "test_session_123",
            "game_reference": "game_ref_001",
            "game_level": 1,
            "game_mode": "classic",
            "game_color": "blue",
            "game_sequence": ["red", "blue", "green"],
            "game_player_input": ["red", "blue"]
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["event_type"], "game_pause")

    def test_delete_game_data_anonymous_denied(self):
        """Test that anonymous users cannot delete game data"""
        url = reverse("game-data-rud", kwargs={"pk": self.game_data.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_game_data_admin_allowed(self):
        """Test that admin users can delete game data"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.admin_token.key}")
        url = reverse("game-data-rud", kwargs={"pk": self.game_data.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(GameData.objects.count(), 0)