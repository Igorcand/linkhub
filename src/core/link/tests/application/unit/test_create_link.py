from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.link.application.use_cases.create_link import CreateLink
from src.core.link.application.use_cases.exceptions import InvalidLinkData
from src.core.user.application.use_cases.exceptions import UserNotFound

from src.core.link.domain.link_repository import LinkRepository
from src.core.user.domain.user_repository import UserRepository
from src.core.user.domain.user import User


import pytest

@pytest.mark.link
class TestCreateLink:
    def test_create_link_with_valid_data(self):
        mock_repository = MagicMock(LinkRepository)
        mock_user_repository = MagicMock(UserRepository)

        user = User(
            id=uuid4(),
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        mock_user_repository.get_by_id.return_value = user
        use_case = CreateLink(repository=mock_repository, user_repository=mock_user_repository)
        request = CreateLink.Input(
            url="www.google.com", 
            user_id=uuid4()
            )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateLink.Output)
        assert isinstance(response.id, UUID)
        assert mock_repository.create.called is True
    
    def test_create_link_with_no_data_provided(self):
        mock_repository = MagicMock(LinkRepository)
        mock_user_repository = MagicMock(UserRepository)

        use_case = CreateLink(repository=mock_repository, user_repository=mock_user_repository)
        with pytest.raises(TypeError) as exc_info:
            response = use_case.execute(CreateLink.Input())

    def test_create_link_with_invalid_data(self):
        mock_repository = MagicMock(LinkRepository)
        mock_user_repository = MagicMock(UserRepository)

        use_case = CreateLink(repository=mock_repository, user_repository=mock_user_repository)
        with pytest.raises(InvalidLinkData, match="url cannot be empty") as exc_info:
            response = use_case.execute(CreateLink.Input(url="", user_id=uuid4()))
    
    def test_create_link_with_user_not_existing(self):
        mock_repository = MagicMock(LinkRepository)
        mock_user_repository = MagicMock(UserRepository)
        mock_user_repository.get_by_id.return_value = None

        use_case = CreateLink(repository=mock_repository, user_repository=mock_user_repository)
        request = CreateLink.Input(
            url="www.google.com", 
            user_id=uuid4()
            )
        with pytest.raises(UserNotFound) as exc_info:
            
            response = use_case.execute(request)