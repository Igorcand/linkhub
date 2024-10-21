from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework_simplejwt.tokens import RefreshToken
from src.django_project.user_app.auth import authenticate
from src.django_project.user_app.serializers import CreateUserRequestSerializer, CreateUserResponseSerializer,  DeleteUserRequestSerializer, UpdatePartialUserRequestSerializer
from src.django_project.user_app.repository import DjangoORMUserRepository
from src.core.user.application.use_cases.create_user import CreateUser
from src.core.user.application.use_cases.delete_user import DeleteUser
from src.core.user.application.use_cases.update_user import UpdateUser
from src.core.user.application.use_cases.exceptions import UserNotFound, UsernameUnavailable
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from uuid import UUID

class UserRegisterViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny,]

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

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def destroy(self,request: Request, pk=None) -> Response:
        serializer = DeleteUserRequestSerializer(data={"id":pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteUser.Input(**serializer.validated_data)
        use_case = DeleteUser(repository=DjangoORMUserRepository())
        try:
            use_case.execute(request=input)
        except UserNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    def partial_update(self, request, pk: UUID = None) -> Response:
        serializer = UpdatePartialUserRequestSerializer(
            data={
                **request.data, 
                "id":pk
                }
            )
        serializer.is_valid(raise_exception=True)

        input = UpdateUser.Input(**serializer.validated_data)
        use_case = UpdateUser(repository=DjangoORMUserRepository())
        try:
            use_case.execute(request=input)
        except (ValueError, UsernameUnavailable) as err:
            return Response(data={"error": str(err)}, status=HTTP_400_BAD_REQUEST)
        except UserNotFound as err:
            return Response(data={"error": str(err)}, status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )