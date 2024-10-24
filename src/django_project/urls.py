"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from src.django_project.user_app.views import UserRegisterViewSet, UserViewSet
from src.django_project.auth_app.views import  CustomTokenObtainPairView, CustomTokenRefreshView

from src.django_project.room_app.views import RoomViewSet
from src.django_project.link_app.views import LinkViewSet
from src.django_project.post_app.views import PostViewSet

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Sua API",
      default_version='v1',
      description="Documentação da sua API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contato@exemplo.com"),
      license=openapi.License(name="Licença MIT"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"api/register", UserRegisterViewSet, basename="register")
router.register(r"api/user", UserViewSet, basename="user")
router.register(r"api/room", RoomViewSet, basename="room")
router.register(r"api/link", LinkViewSet, basename="link")
router.register(r"api/post", PostViewSet, basename="post")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + router.urls
