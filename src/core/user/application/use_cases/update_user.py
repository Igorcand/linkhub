from uuid import UUID
from dataclasses import dataclass
from src.core.user.domain.user import User
from src.core.user.domain.user_repository import UserRepository
from src.core.user.application.use_cases.exceptions import UserNotFound, UsernameUnavailable, InvalidUserData

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


        if request.qnt_room is not None:
            try:
                user.update_qnt_room(
                    qnt_room=request.qnt_room,
                    )
            except ValueError as err:
                raise InvalidUserData(err)
    
        if request.username is not None: 
            username_search = self.repository.get_by_username(username=request.username)
            if username_search is not None and username_search.id != user.id :
                raise UsernameUnavailable(f"Username {request.username} already in use")
        
            try:
                user.update_username(
                    username=request.username,
                    )
            except ValueError as err:
                raise InvalidUserData(err)
        
        self.repository.update(user)
    