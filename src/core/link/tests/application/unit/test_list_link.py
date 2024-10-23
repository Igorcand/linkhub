from unittest.mock import create_autospec
from src.core.link.application.use_cases.list_link import ListLink, LinkOutput
from src.core.link.domain.link_repository import LinkRepository
from src.core.link.domain.link import Link
import pytest
from uuid import uuid4

@pytest.mark.link
class TestListLink:
    def test_when_no_links_in_repository_then_return_empty_list(self):
        mock_repository = create_autospec(LinkRepository)
        mock_repository.list.return_value = []

        use_case = ListLink(repository=mock_repository)
        input = ListLink.Input(user_id=uuid4())
        response = use_case.execute(input)

        assert response == ListLink.Output(
            data=[]
            )
    
    def test_when_categories_in_repository_then_return_list(self):
        user_id = uuid4()
        link = Link(
            url="www.google.com", 
            user_id=user_id, 
        )
        mock_repository = create_autospec(LinkRepository)
        mock_repository.list.return_value = [link]

        use_case = ListLink(repository=mock_repository)
        input = ListLink.Input(user_id=user_id)
        response = use_case.execute(input)

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
    