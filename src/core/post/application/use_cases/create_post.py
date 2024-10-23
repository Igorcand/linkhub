from uuid import UUID
from dataclasses import dataclass, field
from src.core.post.application.use_cases.exceptions import InvalidPostData, PostLimitReached
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.room.application.use_cases.exceptions import RoomNotFound
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.link.application.use_cases.exceptions import RelatedLinksNotFoundForUser


from src.core.room.domain.room_repository import RoomRepository
from src.core.user.domain.user_repository import UserRepository
from src.core.post.domain.post_repository import PostRepository
from src.core.link.domain.link_repository import LinkRepository


from src.core.post.domain.post import Post

class CreatePost:
    def __init__(self, repository: PostRepository, user_repository: UserRepository, room_repository: RoomRepository, link_repository: LinkRepository) -> None:
        self.repository = repository
        self.user_repository = user_repository
        self.room_repository = room_repository
        self.link_repository = link_repository


    @dataclass
    class Input:
        user_id: UUID
        room_id: UUID
        title: str
        links: set[UUID] = field(default_factory=set)
        body: str = ""


    @dataclass
    class Output:
        id: UUID


    def execute(self, input: Input):
        user = self.user_repository.get_by_id(id=input.user_id)
        if user is None:
            raise UserNotFound(f"User with {input.user_id} not found")
        
        room = self.room_repository.get_by_id(id=input.room_id)
        if room is None:
            raise RoomNotFound(f"Room with {input.room_id} not found")
        
        links_ids = {link.id for link in self.link_repository.list(user_id=input.user_id)}
        if not input.links.issubset(links_ids):
            raise RelatedLinksNotFoundForUser(
                f"Links not found: {input.links - links_ids}"
            )
        
        exist_post = self.repository.validate_if_user_id_has_post_in_room_id(user_id=input.user_id, room_id=input.room_id)

        if exist_post is True:
            raise PostLimitReached(f"User with {input.user_id} already has some post in the room {input.room_id}")
        
        try:
            post = Post(
                user_id = input.user_id,
                room_id = input.room_id,
                links = input.links,

                title = input.title,
                body = input.body,

            )
        except ValueError as e:
            raise InvalidPostData(e)
        
        self.repository.create(post)
        return self.Output(id=post.id)