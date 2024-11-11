from abc import ABC, abstractmethod
from uuid import UUID
from src.core.room.domain.room import Room

class RoomRepository(ABC):
    @abstractmethod
    def create(self, room):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> Room | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, room: Room) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Room]:
        raise NotImplementedError