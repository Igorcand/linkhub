from uuid import UUID
from dataclasses import dataclass
from src.core.user.application.use_cases.exceptions import InvalidUserData
from src.core.user.domain.user_repository import UserRepository
from src.core.user.domain.user import User

class CreateUser:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        name: str
        username: str
        email: str
        password: str

    @dataclass
    class Output:
        id: UUID


    def execute(self, input: Input):
        try:
            user = User(
                name = input.name,
                username = input.username,
                email = input.email,
                password = input.password,
            )
        except ValueError as e:
            raise InvalidUserData(e)
        
        self.repository.create(user)
        return self.Output(id=user.id)