from uuid import UUID
from dataclasses import dataclass
from src.core.room.application.use_cases.exceptions import InvalidRoomData, RoomNotFound, RoomInsufficient
from src.core.room.domain.room_repository import RoomRepository
from src.core.user.domain.user_repository import UserRepository
from src.core.user.application.use_cases.exceptions import UserNotFound


from src.core.room.domain.room import Room

class DeleteRoom:
    def __init__(self, repository: RoomRepository, user_repository: UserRepository) -> None:
        self.repository = repository
        self.user_repository = user_repository

    @dataclass
    class Input:
        id: UUID
        user_id: UUID

    def execute(self, input: Input):
        user = self.user_repository.get_by_id(input.user_id)
        if user is None:
            raise UserNotFound(f"User with {input.user_id} not found")

        room = self.repository.get_by_id(input.id)
        if room is None:
            raise RoomNotFound(f"Room with {input.id} not found")


        user.qnt_room -= 1
        try:
            user.validate()
        except ValueError as e:
            if str(e) == "qnt_room cannot be lower than 0":
                raise RoomInsufficient(e)
            raise InvalidRoomData(e)

        self.user_repository.update(user)

        
        self.repository.delete(room.id)