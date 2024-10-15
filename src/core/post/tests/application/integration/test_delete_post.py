from uuid import uuid4
from unittest.mock import create_autospec
from src.core.post.domain.post_repository import PostRepository
from src.core.post.domain.post import Post
from src.core.post.application.use_cases.delete_post import DeletePost
import pytest
from src.core.post.application.use_cases.exceptions import PostNotFound
from src.core.post.infra.in_memory_post_repository import InMemoryPostRepository

@pytest.mark.post
class TestDeletePost:
    def test_delete_post_from_repository(self):
        post = Post(
            room_id=uuid4(),
            user_id=uuid4(), 
            title="MyPost",
            body = "",
            links = [uuid4(), uuid4()]
            )

        repository = InMemoryPostRepository(posts=[post])

        use_case = DeletePost(repository)
        request = use_case.execute(DeletePost.Input(id=post.id))

        assert repository.get_by_id(post.id) is None
        assert request is None

    def test_when_post_not_found_then_raise_exception(self):
        repository = InMemoryPostRepository()
        use_case = DeletePost(repository)
        with pytest.raises(PostNotFound):
            use_case.execute(DeletePost.Input(id=uuid4()))
        
