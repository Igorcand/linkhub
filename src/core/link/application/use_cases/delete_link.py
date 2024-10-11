from uuid import UUID
from dataclasses import dataclass
from src.core.link.application.use_cases.exceptions import InvalidLinkData, LinkNotFound
from src.core.link.domain.link_repository import LinkRepository

from src.core.link.domain.link import Link

class DeleteLink:
    def __init__(self, repository: LinkRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input):
        link = self.repository.get_by_id(input.id)
        if link is None:
            raise LinkNotFound(f"Link with {input.id} not found")
        
        self.repository.delete(link)