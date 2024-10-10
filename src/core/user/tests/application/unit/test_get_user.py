from unittest.mock import create_autospec
from uuid import uuid4
from src.core.user.application.use_cases.get_user import GetUser
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.user.domain.user_repository import UserRepository
from src.core.user.domain.user import User
import pytest

@pytest.mark.user
class TestGetUser:
    def test_return_found_user(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        mock_repository = create_autospec(UserRepository)
        mock_repository.get_by_id.return_value = user

        use_case = GetUser(repository=mock_repository)
        request = GetUser.Input(id=user.id)
        response = use_case.execute(request)

        assert response == GetUser.Output(
            id=user.id,
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            qnt_room=0

        )
    
    def test_when_user_not_found_then_raise_exception(self):
        mock_repository = create_autospec(UserRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetUser(repository=mock_repository)
        request = GetUser.Input(id=uuid4())

        with pytest.raises(UserNotFound):
            use_case.execute(request)


    