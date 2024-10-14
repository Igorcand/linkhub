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
    def get_by_user_id(self, user_id: UUID) -> Post | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, post: Post) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Post]:
        raise NotImplementedError