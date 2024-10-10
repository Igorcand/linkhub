from uuid import UUID
from src.core.link.domain.link import Link
from src.core.link.domain.link_repository import LinkRepository

class InMemoryLinkRepository(LinkRepository):
    def __init__(self, links=None) -> None:
        self.links = links or []
    
    def create(self, link) -> None:
        self.links.append(link)
    
    def get_by_id(self, id: UUID) -> Link | None:
        for link in self.links:
            if link.id == id:
                return link
        return None
    
    def delete(self, id: UUID) -> None:
        link = self.get_by_id(id)
        self.links.remove(link)
    
    def list(self) -> list[Link]:
        return [link for link in self.links]