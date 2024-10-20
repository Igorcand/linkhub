from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework_simplejwt.authentication import JWTAuthentication

from src.core.room.application.use_cases.exceptions import InvalidRoomData, RoomLimitReached

from src.django_project.user_app.repository import DjangoORMUserRepository
from src.django_project.room_app.repository import DjangoORMRoomRepository

from src.django_project.room_app.serializers import CreateRoomRequestSerializer, CreateRoomResponseSerializer

from src.core.room.application.use_cases.create_room import CreateRoom


class RoomViewSet(viewsets.ViewSet):

    def create(self, request: Request) -> Response:    


        serializer = CreateRoomRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        use_case = CreateRoom(
            repository=DjangoORMRoomRepository(), 
            user_repository=DjangoORMUserRepository())
        
        try:
            name = serializer.validated_data['name']

            output = use_case.execute(input=CreateRoom.Input(name=name, user_id=user_id))
        except (InvalidRoomData, RoomLimitReached) as err:
            return Response(data={"error": str(err)}, status=HTTP_400_BAD_REQUEST)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateRoomResponseSerializer(instance=output).data
        )
    