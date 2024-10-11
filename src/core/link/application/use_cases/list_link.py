from uuid import UUID
from dataclasses import dataclass, field
from src.core.link.domain.link import Link
from src.core.link.domain.link_repository import LinkRepository
from src.core.link.application.use_cases.exceptions import LinkNotFound
from src.core._shered.domain.pagination import ListOutputMeta, ListOutput
from src import config
from enum import StrEnum


class ListLink:

    @dataclass
    class Input:
        pass
    
    @dataclass
    class Output:
        id: UUID
        url: str
        user_id: UUID
        
    @dataclass
    class ListLinkResponse():
        data: list[Output]
        meta: list

    def __init__(self, repository: LinkRepository) -> None:
        self.repository = repository

    def execute(self, request: Input) ->ListLinkResponse:
        links = self.repository.list()
        data = [
                Output(
                    id=link.id,
                    url=link.url,
                    user_id=link.user_id,
                ) for link in links
            ]

        return ListLinkResponse(
            data = data,
            meta = []
            )
    