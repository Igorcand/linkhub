from uuid import UUID
from dataclasses import dataclass
from src.core.user.domain.user_repository import UserRepository
from src.core.user.application.use_cases.exceptions import UserNotFound


class DeleteUser:

    @dataclass
    class Input:
        id: UUID

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, request: Input) -> None:
        user = self.repository.get_by_id(id=request.id)
        if user is None:
            raise UserNotFound(f"User with {request.id} not found")

        self.repository.delete(user.id)
    