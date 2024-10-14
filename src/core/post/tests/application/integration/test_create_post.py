from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.post.application.use_cases.create_post import CreatePost

from src.core.room.application.use_cases.exceptions import InvalidRoomData, RoomNotFound
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.link.application.use_cases.exceptions import RelatedLinksNotFound
from src.core.post.application.use_cases.exceptions import InvalidPostData, PostLimitReached

from src.core.room.infra.in_memory_room_repository import InMemoryRoomRepository
from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.link.infra.in_memory_link_repository import InMemoryLinkRepository
from src.core.post.infra.in_memory_post_repository import InMemoryPostRepository

from src.core.room.domain.room import Room
from src.core.user.domain.user import User
from src.core.link.domain.link import Link
from src.core.post.domain.post import Post

import pytest

@pytest.mark.post
class TestCreatePost:
    def test_create_post_with_no_data_provided(self):
        repository = InMemoryPostRepository()
        user_repository = InMemoryUserRepository()
        link_repository = InMemoryLinkRepository()
        room_repository = InMemoryRoomRepository()


        use_case = CreatePost(repository=repository, user_repository=user_repository, link_repository=link_repository, room_repository=room_repository)
        with pytest.raises(TypeError) as exc_info:
            response = use_case.execute(CreatePost.Input())

    def test_create_post_with_user_not_existing(self):
        repository = InMemoryPostRepository()
        user_repository = InMemoryUserRepository()
        link_repository = InMemoryLinkRepository()
        room_repository = InMemoryRoomRepository()

        use_case = CreatePost(repository=repository, user_repository=user_repository, link_repository=link_repository, room_repository=room_repository)
        request = CreatePost.Input(
            user_id=uuid4(),
            room_id=uuid4(),
            links=[uuid4()],
            title="My Post"
            )
        with pytest.raises(UserNotFound) as exc_info:
            response = use_case.execute(request)
    
    def test_create_post_with_room_not_existing(self):

        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        repository = InMemoryPostRepository()
        user_repository = InMemoryUserRepository(users=[user])
        link_repository = InMemoryLinkRepository()
        room_repository = InMemoryRoomRepository()

        use_case = CreatePost(repository=repository, user_repository=user_repository, link_repository=link_repository, room_repository=room_repository)
        request = CreatePost.Input(
            user_id=user.id,
            room_id=uuid4(),
            links={uuid4()},
            title="My Post"
            )
        with pytest.raises(RoomNotFound) as exc_info:
            response = use_case.execute(request)
    
    def test_create_post_with_not_related_links(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )

        room = Room(
            name="Study Room",
            user_id=user.id
        )
        
        repository = InMemoryPostRepository()
        user_repository = InMemoryUserRepository(users=[user])
        link_repository = InMemoryLinkRepository()
        room_repository = InMemoryRoomRepository(rooms=[room])

        use_case = CreatePost(repository=repository, user_repository=user_repository, link_repository=link_repository, room_repository=room_repository)
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

        room = Room(
            name="Study Room",
            user_id=user.id
        )

        post= Post(
            room_id=room.id,
            user_id=user.id,
            title="My Post",
            body="",
            links=[]
        )

        repository = InMemoryPostRepository(posts=[post])
        user_repository = InMemoryUserRepository(users=[user])
        link_repository = InMemoryLinkRepository()
        room_repository = InMemoryRoomRepository(rooms=[room])

        use_case = CreatePost(repository=repository, user_repository=user_repository, link_repository=link_repository, room_repository=room_repository)
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

        room = Room(
            name="Study Room",
            user_id=user.id
        )

        link = Link(
            user_id=user.id,
            url="www.google.com"
        )
        
        repository = InMemoryPostRepository()
        user_repository = InMemoryUserRepository(users=[user])
        link_repository = InMemoryLinkRepository(links=[link])
        room_repository = InMemoryRoomRepository(rooms=[room])

        use_case = CreatePost(repository=repository, user_repository=user_repository, link_repository=link_repository, room_repository=room_repository)
        request = CreatePost.Input(
            user_id=user.id,
            room_id=room.id,
            links={link.id},
            title="My Post"
            )
        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreatePost.Output)
        assert isinstance(response.id, UUID)
        
        persisted_post = repository.get_by_id(response.id)

        print(f"persisted_post = {persisted_post}")

        assert persisted_post.id == response.id
        assert persisted_post.title == "My Post"


    
