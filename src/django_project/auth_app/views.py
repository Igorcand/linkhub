from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from src.django_project.auth_app.serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    pass