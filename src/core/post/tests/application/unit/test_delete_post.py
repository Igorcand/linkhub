from uuid import uuid4
from unittest.mock import create_autospec
from src.core.post.domain.post_repository import PostRepository
from src.core.post.domain.post import Post
from src.core.post.application.use_cases.delete_post import DeletePost
import pytest
from src.core.post.application.use_cases.exceptions import PostNotFound

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

        mock_repository = create_autospec(PostRepository)
        mock_repository.get_by_id.return_value = post

        use_case = DeletePost(mock_repository)
        use_case.execute(DeletePost.Input(id=post.id))

        mock_repository.delete.assert_called_once_with(post.id)

    def test_when_post_not_found_then_raise_exception(self):
        mock_repository = create_autospec(PostRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeletePost(mock_repository)

        with pytest.raises(PostNotFound):
            use_case.execute(DeletePost.Input(id=uuid4()))
        
        mock_repository.delete.assert_not_called() 
        assert mock_repository.delete.called is False