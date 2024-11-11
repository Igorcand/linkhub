from uuid import uuid4
from unittest.mock import create_autospec
from src.core.post.domain.post_repository import PostRepository
from src.core.post.domain.post import Post
from src.core.post.application.use_cases.list_post import ListPost
import pytest
from src.core.post.application.use_cases.exceptions import PostNotFound
from src.core.post.infra.in_memory_post_repository import InMemoryPostRepository

@pytest.mark.post
class TestListPost:
    def test_list_post_by_room(self):
        room_id = uuid4()
        post1 = Post(
            room_id=room_id,
            user_id=uuid4(), 
            title="MyPost",
            body = "",
            links = [uuid4(), uuid4()]
            )
        
        post2 = Post(
            room_id=room_id,
            user_id=uuid4(), 
            title="MyPost2",
            body = "",
            links = [uuid4(), uuid4()]
            )
        
        post3 = Post(
            room_id=uuid4(),
            user_id=uuid4(), 
            title="MyPost3",
            body = "",
            links = [uuid4(), uuid4()]
            )

        repository = InMemoryPostRepository(posts=[post1, post2, post3])

        use_case = ListPost(repository)
        response = use_case.execute(ListPost.Input(room_id=room_id))

        assert len(response.data) == 2


