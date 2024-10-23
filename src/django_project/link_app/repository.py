from src.core.link.domain.link_repository import LinkRepository
from src.django_project.link_app.models import Link as LinkORM
from src.django_project.user_app.models import User as UserORM

from src.core.link.domain.link import Link
from uuid import UUID
from typing import List, Optional
from django.db import transaction

class DjangoORMLinkRepository(LinkRepository):
    def __init__(self, model: LinkORM | None = None) -> None:
        self.model = model or LinkORM

    def create(self, link: Link) -> None: 
        user = UserORM.objects.get(id=link.user_id)   
        link_orm= LinkORM(
            id=link.id,
            url=link.url,
            user_id = user,
            )
        link_orm.save()

    def get_by_id(self, id: UUID) -> Optional[Link]:
        try:
            link = self.model.objects.get(id=id)
            return LinkModelMapper.to_entity(link)
        except self.model.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        return self.model.objects.filter(id=id).delete()

    def list(self, user_id: UUID) -> List[Link]:
        links = LinkORM.objects.filter(user_id=user_id)
        return [
            LinkModelMapper.to_entity(link_model)
            for link_model in links]

class LinkModelMapper:
    @staticmethod
    def to_model(link: Link) -> LinkORM:
        return LinkORM(
            id=link.id,
            url=link.url,
            user_id = link.user_id,

        )
    
    def to_entity(link: LinkORM) -> Link:
        return Link(
            id=link.id,
            url=link.url,
            user_id = link.user_id.id,
        )