from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,    # handles login — returns access + refresh token
    TokenRefreshView,       # handles token refresh — returns new access token
)
from .views import RegisterView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # POST /api/auth/register/ → RegisterView

    path('login/', TokenObtainPairView.as_view(), name='login'),
    # POST /api/auth/login/ → DRF SimpleJWT handles this automatically
    # We don't write login logic — JWT library does it for us!

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # POST /api/auth/token/refresh/ → get new access token using refresh token

    path('profile/', ProfileView.as_view(), name='profile'),
    # GET /api/auth/profile/ → ProfileView (protected)
]