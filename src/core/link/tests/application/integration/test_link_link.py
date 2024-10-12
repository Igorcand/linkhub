from unittest.mock import create_autospec
from src.core.link.application.use_cases.list_link import ListLink, LinkOutput
from src.core.link.domain.link_repository import LinkRepository
from src.core.link.domain.link import Link
import pytest
from uuid import uuid4
from src.core.link.infra.in_memory_link_repository import InMemoryLinkRepository

@pytest.mark.link
class TestListLink:
    def test_when_no_links_in_repository_then_return_empty_list(self):
        repository = InMemoryLinkRepository()

        use_case = ListLink(repository=repository)
        response = use_case.execute(ListLink.Input())

        assert response == ListLink.Output(
            data=[]
            )
    
    def test_when_categories_in_repository_then_return_list(self):
        link = Link(
            url="www.google.com", 
            user_id=uuid4(), 
        )
        repository = InMemoryLinkRepository(links=[link])

        use_case = ListLink(repository=repository)
        response = use_case.execute(ListLink.Input())

        assert response == ListLink.Output(
            data=[
                LinkOutput(
                    id=link.id,
                    url=link.url,
                    user_id=link.user_id,
                    is_valid=link.is_valid
                ),
            ]
        )
    