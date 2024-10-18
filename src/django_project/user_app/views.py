from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework_simplejwt.tokens import RefreshToken

from src.django_project.user_app.auth import authenticate
from src.django_project.user_app.serializers import CreateUserRequestSerializer, CreateUserResponseSerializer, LoginRequestSerializer, LoginResponseSerializer
from src.django_project.user_app.repository import DjangoORMUserRepository

from src.core.user.application.use_cases.create_user import CreateUser

class UserRegisterViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        serializer = CreateUserRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input = CreateUser.Input(**serializer.validated_data)
        use_case = CreateUser(repository=DjangoORMUserRepository())
        try:
            output = use_case.execute(input=input)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=HTTP_400_BAD_REQUEST
            )

        return Response(
            status=HTTP_201_CREATED,
            data=CreateUserResponseSerializer(instance=output).data
        )

class UserLoginViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        authenticated, user = authenticate(email=email, raw_password=password)

        if authenticated:
            refresh = RefreshToken.for_user(user)
            return Response(
                status=HTTP_200_OK,
                data=LoginResponseSerializer(instance={'refresh': str(refresh), 'access': str(refresh.access_token)}).data
            )
        else:
            return Response(
                {"detail": "Invalid credentials"},
                status=HTTP_400_BAD_REQUEST
            )

