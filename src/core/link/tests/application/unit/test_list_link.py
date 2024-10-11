from unittest.mock import create_autospec
from src.core.link.application.use_cases.list_link import ListLink
from src.core._shered.domain.pagination import ListOutputMeta
from src.core.link.domain.link_repository import LinkRepository
from src.core.link.domain.link import Link
import pytest

@pytest.mark.link
class TestListLink:
    def test_when_no_links_in_repository_then_return_empty_list(self):
        mock_repository = create_autospec(LinkRepository)
        mock_repository.list.return_value = []

        use_case = ListLink(repository=mock_repository)
        request = ListLinkRequest()
        response = use_case.execute(ListLink.Input())

        assert response == ListLinkResponse(
            data=[],
            meta = []
            )
    
    def test_when_categories_in_repository_then_return_list(self):
        link = Link(
            url="www.google.com", 
            user_id=uuid4(), 
        )
        mock_repository = create_autospec(LinkRepository)
        mock_repository.list.return_value = [link]

        use_case = ListLink(repository=mock_repository)
        response = use_case.execute(ListLink.Input())

        assert response == ListLinkResponse(
            data=[
                ListLink.Output(
                    id=link.id,
                    url=link.url,
                    user_id=link.user_id
                ),
            ],
            meta = []
        )
    