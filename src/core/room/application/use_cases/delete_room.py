from uuid import UUID
from dataclasses import dataclass
from src.core.room.application.use_cases.exceptions import InvalidRoomData, RoomNotFound
from src.core.room.domain.room_repository import RoomRepository

from src.core.room.domain.room import Room

class DeleteRoom:
    def __init__(self, repository: RoomRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input):
        room = self.repository.get_by_id(input.id)
        if room is None:
            raise RoomNotFound(f"Room with {input.id} not found")
        self.repository.delete(room.id)