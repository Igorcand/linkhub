from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.core.post.application.use_cases.exceptions import InvalidPostData, PostLimitReached
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.room.application.use_cases.exceptions import RoomNotFound
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.link.application.use_cases.exceptions import RelatedLinksNotFoundForUser

from src.django_project.user_app.repository import DjangoORMUserRepository
from src.django_project.room_app.repository import DjangoORMRoomRepository
from src.django_project.link_app.repository import DjangoORMLinkRepository
from src.django_project.post_app.repository import DjangoORMPostRepository


from src.django_project.post_app.serializers import CreatePostRequestSerializer, CreatePostResponseSerializer

from src.core.post.application.use_cases.create_post import CreatePost


from rest_framework.permissions import IsAuthenticated
from uuid import UUID

class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request: Request) -> Response:    
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
        except (RoomNotFound, UserNotFound, RelatedLinksNotFoundForUser) as err:
            return Response(data={"error": str(err)}, status=HTTP_404_NOT_FOUND)
        except (PostLimitReached, InvalidPostData) as err:
            return Response(data={"error": str(err)}, status=HTTP_404_NOT_FOUND)

        return Response(
            status=HTTP_201_CREATED,
            data=CreatePostResponseSerializer(instance=output).data
        )