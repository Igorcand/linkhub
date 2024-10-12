from uuid import UUID
from dataclasses import dataclass, field
from src.core.link.domain.link import Link
from src.core.link.domain.link_repository import LinkRepository
from src.core.link.application.use_cases.exceptions import LinkNotFound

@dataclass
class LinkOutput:
    id: UUID
    url: str
    user_id: UUID
    is_valid: bool

class ListLink:

    @dataclass
    class Input:
        pass
        
    @dataclass
    class Output:
        data: list[LinkOutput]

    def __init__(self, repository: LinkRepository) -> None:
        self.repository = repository

    def execute(self, request: Input) -> Output:
        links = self.repository.list()

        return self.Output(data = [
                LinkOutput(
                    id=link.id,
                    url=link.url,
                    user_id=link.user_id,
                    is_valid=link.is_valid
                ) for link in links
            ])
    