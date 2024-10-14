from uuid import UUID
from dataclasses import dataclass
from src.core.room.application.use_cases.exceptions import InvalidRoomData, RoomLimitReached
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.room.domain.room_repository import RoomRepository
from src.core.user.domain.user_repository import UserRepository

from src.core.room.domain.room import Room

class CreateRoom:
    def __init__(self, repository: RoomRepository, user_repository: UserRepository) -> None:
        self.repository = repository
        self.user_repository = user_repository

    @dataclass
    class Input:
        name: str
        user_id: UUID

    @dataclass
    class Output:
        id: UUID


    def execute(self, input: Input):
        user = self.user_repository.get_by_id(input.user_id)
        if user is None:
            raise UserNotFound(f"User with {input.user_id} not found")
        
        user.qnt_room += 1
        try:
            user.validate()
        except ValueError as e:
            if str(e) == "qnt_room cannot be bigger than 5":
                raise RoomLimitReached(e)
            raise InvalidRoomData(e)

        self.user_repository.update(user)
        try:
            room = Room(
                name = input.name,
                user_id = input.user_id
            )
        except ValueError as e:
            raise InvalidRoomData(e)
        
        self.repository.create(room)
        return self.Output(id=room.id)