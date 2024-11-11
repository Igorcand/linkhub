from uuid import UUID
from dataclasses import dataclass, field
from src.core.room.domain.room import Room
from src.core.room.domain.room_repository import RoomRepository
from src.core.room.application.use_cases.exceptions import RoomNotFound

@dataclass
class RoomOutput:
    id: UUID
    name: str
    user_id: UUID

class ListRoom:

    @dataclass
    class Input:
        pass
        
    @dataclass
    class Output:
        data: list[RoomOutput]

    def __init__(self, repository: RoomRepository) -> None:
        self.repository = repository

    def execute(self, request: Input) -> Output:
        rooms = self.repository.list()

        return self.Output(data = [
                RoomOutput(
                    id=room.id,
                    name=room.name,
                    user_id=room.user_id
                ) for room in rooms
            ])
    