from abc import ABC, abstractmethod
from uuid import UUID
from src.core.post.domain.post import Post

class PostRepository(ABC):
    @abstractmethod
    def create(self, post):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> Post | None:
        raise NotImplementedError
    
    @abstractmethod
    def validate_if_user_id_has_post_in_room_id(self, user_id: UUID) -> list[Post] | None:
        raise NotImplementedError
    
    @abstractmethod
    def list_by_room_id(self, room_id: UUID) -> Post | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError


