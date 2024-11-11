from uuid import UUID
from dataclasses import dataclass
from src.core.user.domain.user import User
from src.core.user.domain.user_repository import UserRepository
from src.core.user.application.use_cases.exceptions import UserNotFound

class GetUser:
    @dataclass
    class Input:
        id: UUID
    
    @dataclass
    class Output:
        id: UUID
        name: str
        username: str 
        email: bool
        qnt_room: bool

        
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, request: Input) -> Output:

        user = self.repository.get_by_id(id=request.id)

        if user is None:
            raise UserNotFound(f"User with {request.id} not found")

        return self.Output(
            id=user.id,
            name=user.name,
            username=user.username,
            email=user.email,
            qnt_room=user.qnt_room
            )
    