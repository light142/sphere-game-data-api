from django.urls import path
from .views import (
    GameDataListCreateView,
    GameDataRetrieveUpdateDestroyView,
    LoginAPIView,
    LogoutAPIView,
)

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("game-data/", GameDataListCreateView.as_view(), name="game-data-list-create"),
    path("game-data/<int:pk>/", GameDataRetrieveUpdateDestroyView.as_view(), name="game-data-rud"),
]
