from uuid import UUID
from dataclasses import dataclass
from src.core.room.domain.room import Room
from src.core.room.domain.room_repository import RoomRepository
from src.core.room.application.use_cases.exceptions import RoomNotFound, InvalidRoomData

class UpdateRoom:

    @dataclass
    class Input:
        id: UUID
        name: str


    def __init__(self, repository: RoomRepository) -> None:
        self.repository = repository

    def execute(self, request: Input) -> None:
        room = self.repository.get_by_id(id=request.id)
        if room is None:
            raise RoomNotFound(f"Room with {request.id} not found")


        try:
            room.update_name(
                name=request.name,
                )
        except ValueError as err:
            raise InvalidRoomData(err)
    
        
        self.repository.update(room)
    