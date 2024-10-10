from uuid import UUID
from dataclasses import dataclass
from src.core.user.domain.user import User
from src.core.user.domain.user_repository import UserRepository
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.user.application.use_cases.exceptions import InvalidUserData

class UpdateUser:

    @dataclass
    class Input:
        id: UUID
        qnt_room: int | None = None
        username: int | None = None


    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, request: Input) -> None:
        user = self.repository.get_by_id(id=request.id)
        if user is None:
            raise UserNotFound(f"User with {request.id} not found")

        current_qnt_room = user.qnt_room
        current_username = user.username

        
        if request.qnt_room is not None: current_qnt_room = request.qnt_room

        if request.username is not None: current_username = request.username


        try:
            user.update_qnt_room(
                qnt_room=current_qnt_room,
                )
        except ValueError as err:
            raise InvalidUserData(err)

        try:
            user.update_username(
                username=current_username,
                )
        except ValueError as err:
            raise InvalidUserData(err)
        
        self.repository.update(user)
    