from uuid import uuid4
from unittest.mock import create_autospec
from src.core.link.domain.link_repository import LinkRepository
from src.core.link.domain.link import Link
from src.core.link.application.use_cases.delete_link import DeleteLink
import pytest
from src.core.link.application.use_cases.exceptions import LinkNotFound
from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.link.infra.in_memory_link_repository import InMemoryLinkRepository

@pytest.mark.link
class TestDeleteLink:
    def test_delete_link_from_repository(self):
        link = Link(
            url="www.google.com", 
            user_id=uuid4(), 
        )
        repository = InMemoryLinkRepository(links=[link])

        use_case = DeleteLink(repository=repository)
        request = use_case.execute(DeleteLink.Input(id=link.id))

        assert repository.get_by_id(link.id) is None
        assert request is None

    def test_when_link_not_found_then_raise_exception(self):
        repository = InMemoryLinkRepository()

        use_case = DeleteLink(repository)

        with pytest.raises(LinkNotFound):
            use_case.execute(DeleteLink.Input(id=uuid4()))
        