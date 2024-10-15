from uuid import UUID
from dataclasses import dataclass
from src.core.post.application.use_cases.exceptions import InvalidPostData, PostNotFound
from src.core.post.domain.post_repository import PostRepository
from src.core.post.domain.post import Post

class DeletePost:
    def __init__(self, repository: PostRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input):
        post = self.repository.get_by_id(input.id)
        if post is None:
            raise PostNotFound(f"Post with {input.id} not found")
        self.repository.delete(post.id)