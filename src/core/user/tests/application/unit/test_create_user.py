from unittest.mock import MagicMock
from uuid import UUID
from src.core.user.application.use_cases.create_user import CreateUser
from src.core.user.application.use_cases.exceptions import InvalidUserData
from src.core.user.domain.user_repository import UserRepository
import pytest

@pytest.mark.user
class TestCreateCateory:
    def test_create_user_with_valid_data(self):
        mock_repository = MagicMock(UserRepository)
        use_case = CreateUser(repository=mock_repository)

        request = CreateUser.Input(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateUser.Output)
        assert isinstance(response.id, UUID)
        assert mock_repository.create.called is True
    
    def test_create_user_with_no_data_provided(self):
        mock_repository = MagicMock(UserRepository)
        use_case = CreateUser(repository=mock_repository)
        with pytest.raises(TypeError) as exc_info:
            response = use_case.execute(CreateUser.Input())

    def test_create_user_with_invalid_data(self):
        mock_repository = MagicMock(UserRepository)
        use_case = CreateUser(repository=mock_repository)
        with pytest.raises(InvalidUserData, match="name cannot be empty") as exc_info:
            response = use_case.execute(CreateUser.Input(name="", username="Teste123", email="test@ulife.com.br", password='123test*'))