from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.django_project.user_app.repository import DjangoORMUserRepository
from src.django_project.link_app.repository import DjangoORMLinkRepository

from src.django_project.link_app.serializers import CreateLinkRequestSerializer, CreateLinkResponseSerializer, ListLinkResponseSerializer, DeleteLinkResponseSerializer

from src.core.link.application.use_cases.create_link import CreateLink
from src.core.link.application.use_cases.delete_link import DeleteLink
from src.core.link.application.use_cases.list_link import ListLink

from src.core.link.application.use_cases.exceptions import InvalidLinkData, LinkNotFound
from src.core.user.application.use_cases.exceptions import UserNotFound


from rest_framework.permissions import IsAuthenticated
from uuid import UUID

class LinkViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> Response:    
        user_id = request.user.id
        serializer = CreateLinkRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        use_case = CreateLink(
            repository=DjangoORMLinkRepository(), 
            user_repository=DjangoORMUserRepository())
        
        try:
            url = serializer.validated_data['url']

            output = use_case.execute(input=CreateLink.Input(url=url, user_id=user_id))
        except UserNotFound as err:
            return Response(data={"error": str(err)}, status=HTTP_404_NOT_FOUND)
        except InvalidLinkData as err:
            return Response(data={"error": str(err)}, status=HTTP_400_BAD_REQUEST)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateLinkResponseSerializer(instance=output).data
        )
    
    def list(self, request: Request) -> Response:
        user_id = request.user.id
        use_case = ListLink(repository=DjangoORMLinkRepository())
        output = use_case.execute(ListLink.Input(user_id=user_id))
        serializer = ListLinkResponseSerializer(instance=output)
        return Response(status=HTTP_200_OK, data=serializer.data)
    
    def destroy(self,request: Request, pk: UUID=None) -> Response:
        serializer = DeleteLinkResponseSerializer(data={"id":pk})
        serializer.is_valid(raise_exception=True)

        input = DeleteLink.Input(id=pk)
        use_case = DeleteLink(
            repository=DjangoORMLinkRepository())
        try:
            use_case.execute(input=input)
        except LinkNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )


    