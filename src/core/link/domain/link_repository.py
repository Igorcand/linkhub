from abc import ABC, abstractmethod
from uuid import UUID
from src.core.link.domain.link import Link

class LinkRepository(ABC):
    @abstractmethod
    def create(self, link):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> Link | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Link]:
        raise NotImplementedError