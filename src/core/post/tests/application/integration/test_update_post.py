from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.post.application.use_cases.update_post import UpdatePost

from src.core.room.application.use_cases.exceptions import InvalidRoomData, RoomNotFound
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.link.application.use_cases.exceptions import RelatedLinksNotFoundForUser
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
class TestUpdatePost:
    def test_update_post_with_all_fields_provided(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )

        link = Link(
            user_id=user.id,
            url="www.google.com"
        )

        link2 = Link(
            user_id=user.id,
            url="www.linkedin.com"
        )
        
        post = Post(
            room_id=uuid4(),
            user_id=user.id,
            title="My Post",
            body="",
            links={link.id}
        )
        repository = InMemoryPostRepository()
        repository.create(post)

        link_repository = InMemoryLinkRepository(links=[link, link2])

        use_case = UpdatePost(repository=repository, link_repository=link_repository)
        request = UpdatePost.Input(
            id=post.id,
            user_id=user.id,
            title="My Post updated",
            body="Body content",
            links={link.id, link2.id},
            )
        use_case.execute(request)
        
        persisted_post = repository.get_by_id(post.id)

        assert persisted_post.id == post.id
        assert persisted_post.title == "My Post updated"
        assert persisted_post.body == "Body content"
        assert persisted_post.links == {link.id, link2.id}
    
    def test_update_post_with_only_body_provided_value(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )

        link = Link(
            user_id=user.id,
            url="www.google.com"
        )

        link2 = Link(
            user_id=user.id,
            url="www.linkedin.com"
        )
        
        post = Post(
            room_id=uuid4(),
            user_id=user.id,
            title="My Post",
            body="",
            links={link.id}
        )
        repository = InMemoryPostRepository()
        repository.create(post)

        link_repository = InMemoryLinkRepository(links=[link, link2])

        use_case = UpdatePost(repository=repository, link_repository=link_repository)
        request = UpdatePost.Input(
            id=post.id,
            user_id=user.id,
            body="Body content",
            )
        use_case.execute(request)
        
        persisted_post = repository.get_by_id(post.id)

        assert persisted_post.id == post.id
        assert persisted_post.title == "My Post"
        assert persisted_post.body == "Body content"
        assert persisted_post.links == {link.id}




    
