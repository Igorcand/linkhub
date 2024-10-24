from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.post.application.use_cases.exceptions import InvalidPostData, PostLimitReached, PostNotFound
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.room.application.use_cases.exceptions import RoomNotFound
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.link.application.use_cases.exceptions import RelatedLinksNotFoundForUser

from src.django_project.user_app.repository import DjangoORMUserRepository
from src.django_project.room_app.repository import DjangoORMRoomRepository
from src.django_project.link_app.repository import DjangoORMLinkRepository
from src.django_project.post_app.repository import DjangoORMPostRepository


from src.django_project.post_app.serializers import CreatePostRequestSerializer, CreatePostResponseSerializer, DeletePostRequestSerializer, ListPostResponseSerializer, UpdatePartialPostRequestSerializer

from src.core.post.application.use_cases.create_post import CreatePost
from src.core.post.application.use_cases.delete_post import DeletePost
from src.core.post.application.use_cases.list_post import ListPost
from src.core.post.application.use_cases.update_post import UpdatePost





from rest_framework.permissions import IsAuthenticated
from uuid import UUID

class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> Response:  
        '''
        Cria um novo post
        '''  
        user_id = request.user.id
        serializer = CreatePostRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        use_case = CreatePost(
            repository=DjangoORMPostRepository(), 
            user_repository=DjangoORMUserRepository(),
            room_repository=DjangoORMRoomRepository(),
            link_repository=DjangoORMLinkRepository())
        
        try:
            title = serializer.validated_data['title']
            body = serializer.validated_data['body']
            room_id = serializer.validated_data['room_id']
            links = serializer.validated_data['links']

            input = CreatePost.Input(
                user_id=user_id,
                room_id=room_id,
                title=title,
                links=links,
                body=body
            )
            output = use_case.execute(input=input)
        except (RoomNotFound, UserNotFound) as err:
            return Response(data={"error": str(err)}, status=HTTP_404_NOT_FOUND)
        except (PostLimitReached, InvalidPostData, RelatedLinksNotFoundForUser) as err:
            return Response(data={"error": str(err)}, status=HTTP_400_BAD_REQUEST)

        return Response(
            status=HTTP_201_CREATED,
            data=CreatePostResponseSerializer(instance=output).data
        )

    def retrieve(self, request: Request, pk=None) -> Response:
        '''
        Retorna todos os post de uma sala
        '''
        use_case = ListPost(repository=DjangoORMPostRepository())
        output = use_case.execute(ListPost.Input(room_id=pk))
        serializer = ListPostResponseSerializer(instance=output)
        return Response(status=HTTP_200_OK, data=serializer.data)
    
    def destroy(self,request: Request, pk: UUID=None) -> Response:
        '''
        Deleta um post
        '''
        serializer = DeletePostRequestSerializer(data={"id":pk})
        serializer.is_valid(raise_exception=True)

        input = DeletePost.Input(id=pk)
        use_case = DeletePost(
            repository=DjangoORMPostRepository())
        try:
            use_case.execute(input=input)
        except PostNotFound as err:
            return Response(data={"error": str(err)}, status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )

    def partial_update(self, request, pk: UUID = None) -> Response:
        '''
        Permite atualizar o título, corpo e links relacionado ao Post
        '''
        user_id = request.user.id
        serializer = UpdatePartialPostRequestSerializer(
            data={
                **request.data, 
                "id":pk
                }
            )
        serializer.is_valid(raise_exception=True)

        
        input = UpdatePost.Input(**serializer.validated_data, user_id=user_id)
        use_case = UpdatePost(repository=DjangoORMPostRepository(), link_repository=DjangoORMLinkRepository())
        try:
            use_case.execute(request=input)
        except (InvalidPostData, RelatedLinksNotFoundForUser) as err:
            return Response(data={"error": str(err)}, status=HTTP_400_BAD_REQUEST)
        except PostNotFound as err:
            return Response(data={"error": str(err)}, status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_204_NO_CONTENT,
        )