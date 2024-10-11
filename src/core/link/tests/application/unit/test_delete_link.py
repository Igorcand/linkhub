from uuid import uuid4
from unittest.mock import create_autospec
from src.core.link.domain.link_repository import LinkRepository
from src.core.link.domain.link import Link
from src.core.link.application.use_cases.delete_link import DeleteLink
import pytest
from src.core.link.application.use_cases.exceptions import LinkNotFound

@pytest.mark.link
class TestDeleteLink:
    def test_delete_link_from_repository(self):
        link = Link(
            url="www.google.com", 
            user_id=uuid4(), 
            )

        mock_repository = create_autospec(LinkRepository)
        mock_repository.get_by_id.return_value = link

        use_case = DeleteLink(mock_repository)
        use_case.execute(DeleteLink.Input(id=link.id))

        mock_repository.delete.assert_called_once_with(link.id)

    def test_when_link_not_found_then_raise_exception(self):
        mock_repository = create_autospec(LinkRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteLink(mock_repository)

        with pytest.raises(LinkNotFound):
            use_case.execute(DeleteLink.Input(id=uuid4()))
        
        mock_repository.delete.assert_not_called() 
        assert mock_repository.delete.called is False