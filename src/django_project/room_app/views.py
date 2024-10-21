from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework_simplejwt.authentication import JWTAuthentication

from src.core.room.application.use_cases.exceptions import InvalidRoomData, RoomLimitReached, RoomNotFound, RoomInsufficient

from src.django_project.user_app.repository import DjangoORMUserRepository
from src.django_project.room_app.repository import DjangoORMRoomRepository

from src.django_project.room_app.serializers import CreateRoomRequestSerializer, CreateRoomResponseSerializer, DeleteRoomRequestSerializer, PartialUpdateRoomRequestSerializer, ListRoomResponseSerializer

from src.core.room.application.use_cases.create_room import CreateRoom
from src.core.room.application.use_cases.delete_room import DeleteRoom
from src.core.room.application.use_cases.update_room import UpdateRoom
from src.core.room.application.use_cases.list_room import ListRoom


from rest_framework.permissions import IsAuthenticated
from uuid import UUID

class RoomViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> Response:    
        user_id = request.user.id
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
    
    def list(self, request: Request) -> Response:
        use_case = ListRoom(repository=DjangoORMRoomRepository())
        output = use_case.execute(ListRoom.Input())
        serializer = ListRoomResponseSerializer(instance=output)
        return Response(status=HTTP_200_OK, data=serializer.data)
    
    def destroy(self,request: Request, pk: UUID=None) -> Response:
        user_id = request.user.id
        serializer = DeleteRoomRequestSerializer(data={"id":pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteRoom.Input(id=pk, user_id=user_id)
        use_case = DeleteRoom(
            repository=DjangoORMRoomRepository(),
            user_repository=DjangoORMUserRepository())
        try:
            use_case.execute(input=input)
        except RoomNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    def partial_update(self, request, pk: UUID = None) -> Response:
        serializer = PartialUpdateRoomRequestSerializer(
            data={
                **request.data, 
                "id":pk
                }
            )
        serializer.is_valid(raise_exception=True)

        input = UpdateRoom.Input(**serializer.validated_data)
        use_case = UpdateRoom(repository=DjangoORMRoomRepository())
        try:
            use_case.execute(request=input)
        except ValueError as err:
            return Response(data={"error": str(err)}, status=HTTP_400_BAD_REQUEST)
        except RoomNotFound as err:
            return Response(data={"error": str(err)}, status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )
    