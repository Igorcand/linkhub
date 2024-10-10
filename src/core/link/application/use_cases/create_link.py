from uuid import UUID
from dataclasses import dataclass
from src.core.link.application.use_cases.exceptions import InvalidLinkData
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.link.domain.link_repository import LinkRepository
from src.core.user.domain.user_repository import UserRepository

from src.core.link.domain.link import Link

class CreateLink:
    def __init__(self, repository: LinkRepository, user_repository: UserRepository) -> None:
        self.repository = repository
        self.user_repository = user_repository

    @dataclass
    class Input:
        url: str
        user_id: UUID

    @dataclass
    class Output:
        id: UUID


    def execute(self, input: Input):
        user = self.user_repository.get_by_id(input.user_id)
        if user is None:
            raise UserNotFound(f"User with {input.user_id} not found")
        
        try:
            link = Link(
                url = input.url,
                user_id = input.user_id
            )
        except ValueError as e:
            raise InvalidLinkData(e)
        
        self.repository.create(link)
        return self.Output(id=link.id)