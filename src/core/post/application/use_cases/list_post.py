from uuid import UUID
from dataclasses import dataclass, field
from src.core.post.domain.post import Post
from src.core.post.domain.post_repository import PostRepository
from src.core.post.application.use_cases.exceptions import PostNotFound

@dataclass
class PostOutput:
    id: UUID
    user_id: UUID
    title: str
    body: str
    links: set[UUID]

class ListPost:

    @dataclass
    class Input:
        room_id: UUID
        
    @dataclass
    class Output:
        data: list[PostOutput]

    def __init__(self, repository: PostRepository) -> None:
        self.repository = repository

    def execute(self, request: Input) -> Output:
        posts = self.repository.list_by_room_id(room_id=request.room_id)

        return self.Output(data = [
                PostOutput(
                    id=post.id,
                    user_id=post.user_id,
                    title=post.title,
                    body=post.body,
                    links=post.links,
                ) for post in posts
            ])
    