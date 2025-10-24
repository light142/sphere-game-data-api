from django.contrib.auth import authenticate, logout
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404

from sphere_game_data_api.models import GameData
from sphere_game_data_api.permissions import IsAdminOrReadOnly

from .serializers import (
    GameDataSerializer,
    LoginSerializer,
    LogoutSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login to get authentication token",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, example="Login successful"),
                        'token': openapi.Schema(type=openapi.TYPE_STRING, example="2033413e311925d9a24241cbf8665fca99168f19")
                    }
                )
            ),
            400: "Invalid credentials"
        },
        security=[]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response(
                    {"message": "Login successful", "token": token.key},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Logout API
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=LogoutSerializer,
        responses={200: "Logged out successfully", 401: "Unauthorized"},
    )
    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )


class GameDataListCreateView(generics.ListCreateAPIView):
    queryset = GameData.objects.all().order_by("-created_at")
    serializer_class = GameDataSerializer
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_description="List all game data (Admin only)",
        responses={200: GameDataSerializer(many=True)},
        security=[{"Token": []}]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new game data entry (Anyone can create)",
        request_body=GameDataSerializer,
        responses={201: GameDataSerializer},
        security=[]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class GameDataRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameData.objects.all()
    serializer_class = GameDataSerializer
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve game data by ID (Admin only)", 
        responses={200: GameDataSerializer},
        security=[{"Token": []}]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update game data by ID (Admin only)",
        request_body=GameDataSerializer,
        responses={200: GameDataSerializer},
        security=[{"Token": []}]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete game data by ID (Admin only)", 
        responses={204: "No Content"},
        security=[{"Token": []}]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


