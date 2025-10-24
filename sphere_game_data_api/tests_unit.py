from django.test import RequestFactory, TestCase
from unittest.mock import patch, MagicMock
from rest_framework.test import force_authenticate
from rest_framework import status

from sphere_game_data_api.views import LoginAPIView  # Replace with your actual path

class LoginAPIViewUnitTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = LoginAPIView.as_view()
        self.url = '/api/login/'
        self.data = {
            "username": "mockuser",
            "password": "MockPass123!"
        }

    @patch('sphere_game_data_api.views.Token')
    @patch('sphere_game_data_api.views.authenticate')
    @patch('sphere_game_data_api.views.LoginSerializer')
    def test_login_success(self, mock_serializer_class, mock_authenticate, mock_token_class):
        # Setup mocked serializer
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.validated_data = self.data
        mock_serializer_class.return_value = mock_serializer

        # Setup mocked user and token
        mock_user = MagicMock()
        mock_authenticate.return_value = mock_user

        mock_token = MagicMock()
        mock_token.key = "mocktoken123"
        mock_token_class.objects.get_or_create.return_value = (mock_token, True)

        request = self.factory.post(self.url, data=self.data, content_type='application/json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Login successful')
        self.assertEqual(response.data['token'], 'mocktoken123')

    @patch('sphere_game_data_api.views.authenticate')
    @patch('sphere_game_data_api.views.LoginSerializer')
    def test_login_invalid_credentials(self, mock_serializer_class, mock_authenticate):
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.validated_data = self.data
        mock_serializer_class.return_value = mock_serializer

        mock_authenticate.return_value = None

        request = self.factory.post(self.url, data=self.data, content_type='application/json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    @patch('sphere_game_data_api.views.LoginSerializer')
    def test_login_invalid_serializer(self, mock_serializer_class):
        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = False
        mock_serializer.errors = {'username': ['This field is required.']}
        mock_serializer_class.return_value = mock_serializer

        request = self.factory.post(self.url, data={}, content_type='application/json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
