from abc import ABC, abstractmethod
from uuid import UUID
from src.core.user.domain.user import User

class UserRepository(ABC):
    @abstractmethod
    def create(self, user):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[User]:
        raise NotImplementedError