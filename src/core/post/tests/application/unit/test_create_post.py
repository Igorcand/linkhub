from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.post.application.use_cases.create_post import CreatePost

from src.core.room.application.use_cases.exceptions import InvalidRoomData, RoomNotFound
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.link.application.use_cases.exceptions import RelatedLinksNotFound
from src.core.post.application.use_cases.exceptions import InvalidPostData, PostLimitReached

from src.core.room.domain.room_repository import RoomRepository
from src.core.user.domain.user_repository import UserRepository
from src.core.link.domain.link_repository import LinkRepository
from src.core.post.domain.post_repository import PostRepository

from src.core.room.domain.room import Room
from src.core.user.domain.user import User
from src.core.link.domain.link import Link
from src.core.post.domain.post import Post

import pytest

@pytest.mark.post
class TestCreatePost:
    def test_create_post_with_no_data_provided(self):
        mock_repository = MagicMock(PostRepository)
        mock_user_repository = MagicMock(UserRepository)
        mock_link_repository = MagicMock(LinkRepository)
        mock_room_repository = MagicMock(RoomRepository)


        use_case = CreatePost(repository=mock_repository, user_repository=mock_user_repository, link_repository=mock_link_repository, room_repository=mock_room_repository)
        with pytest.raises(TypeError) as exc_info:
            response = use_case.execute(CreatePost.Input())

    def test_create_post_with_user_not_existing(self):
        mock_repository = MagicMock(PostRepository)
        mock_link_repository = MagicMock(LinkRepository)
        mock_room_repository = MagicMock(RoomRepository)
        mock_user_repository = MagicMock(UserRepository)
        mock_user_repository.get_by_id.return_value = None

        use_case = CreatePost(repository=mock_repository, user_repository=mock_user_repository, link_repository=mock_link_repository, room_repository=mock_room_repository)
        request = CreatePost.Input(
            user_id=uuid4(),
            room_id=uuid4(),
            links=[uuid4()],
            title="My Post"
            )
        with pytest.raises(UserNotFound) as exc_info:
            response = use_case.execute(request)
    
    def test_create_post_with_room_not_existing(self):
        mock_repository = MagicMock(PostRepository)

        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        mock_user_repository = MagicMock(UserRepository)
        mock_user_repository.get_by_id.return_value = user

        mock_link_repository = MagicMock(LinkRepository)
        mock_room_repository = MagicMock(RoomRepository)
        mock_room_repository.get_by_id.return_value = None

        use_case = CreatePost(repository=mock_repository, user_repository=mock_user_repository, link_repository=mock_link_repository, room_repository=mock_room_repository)
        request = CreatePost.Input(
            user_id=user.id,
            room_id=uuid4(),
            links={uuid4()},
            title="My Post"
            )
        with pytest.raises(RoomNotFound) as exc_info:
            response = use_case.execute(request)
    
    def test_create_post_with_not_related_links(self):
        mock_repository = MagicMock(PostRepository)

        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        mock_user_repository = MagicMock(UserRepository)
        mock_user_repository.get_by_id.return_value = user

        room = Room(
            name="Study Room",
            user_id=user.id
        )
        mock_room_repository = MagicMock(RoomRepository)
        mock_room_repository.get_by_id.return_value = room

        mock_link_repository = MagicMock(LinkRepository)
        mock_link_repository.list.return_value = []

        use_case = CreatePost(repository=mock_repository, user_repository=mock_user_repository, link_repository=mock_link_repository, room_repository=mock_room_repository)
        request = CreatePost.Input(
            user_id=user.id,
            room_id=room.id,
            links={uuid4()},
            title="My Post"
            )
        with pytest.raises(RelatedLinksNotFound) as exc_info:
            response = use_case.execute(request)

    def test_create_post_with_alredy_existing_post_in_room(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        mock_user_repository = MagicMock(UserRepository)
        mock_user_repository.get_by_id.return_value = user

        room = Room(
            name="Study Room",
            user_id=user.id
        )
        mock_room_repository = MagicMock(RoomRepository)
        mock_room_repository.get_by_id.return_value = room

        mock_link_repository = MagicMock(LinkRepository)
        mock_link_repository.list.return_value = []

        mock_repository = MagicMock(PostRepository)
        mock_repository.get_by_user_id.return_value = user

        use_case = CreatePost(repository=mock_repository, user_repository=mock_user_repository, link_repository=mock_link_repository, room_repository=mock_room_repository)
        request = CreatePost.Input(
            user_id=user.id,
            room_id=room.id,
            links=set(),
            title="My Post"
            )
        with pytest.raises(PostLimitReached) as exc_info:
            response = use_case.execute(request)

    def test_create_post_with_provided_values(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        mock_user_repository = MagicMock(UserRepository)
        mock_user_repository.get_by_id.return_value = user

        room = Room(
            name="Study Room",
            user_id=user.id
        )
        mock_room_repository = MagicMock(RoomRepository)
        mock_room_repository.get_by_id.return_value = room

        mock_link_repository = MagicMock(LinkRepository)
        mock_link_repository.list.return_value = []

        mock_repository = MagicMock(PostRepository)
        mock_repository.get_by_user_id.return_value = None

        use_case = CreatePost(repository=mock_repository, user_repository=mock_user_repository, link_repository=mock_link_repository, room_repository=mock_room_repository)
        request = CreatePost.Input(
            user_id=user.id,
            room_id=room.id,
            links=set(),
            title="My Post"
            )
        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreatePost.Output)
        assert isinstance(response.id, UUID)
        assert mock_repository.create.called is True

    
