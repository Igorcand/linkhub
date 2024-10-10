from unittest.mock import create_autospec
from uuid import uuid4
from src.core.user.application.use_cases.update_user import UpdateUser
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.user.domain.user_repository import UserRepository
from src.core.user.domain.user import User
import pytest

@pytest.mark.user
class TestUpdateUser:
    def test_update_user_username(self):
        user = User(
            id=uuid4(),
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        mock_repository = create_autospec(UserRepository)
        mock_repository.get_by_id.return_value = user

        use_case = UpdateUser(repository=mock_repository)
        request = UpdateUser.Input(
            id=user.id,
            username="Teste2"
            )
        
        use_case.execute(request)

        assert user.username == "Teste2"
        assert user.name == "Teste"
        mock_repository.update.assert_called_once_with(user)

    def test_update_qnt_room(self):
        user = User(
            id=uuid4(),
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        mock_repository = create_autospec(UserRepository)
        mock_repository.get_by_id.return_value = user

        use_case = UpdateUser(repository=mock_repository)
        request = UpdateUser.Input(
            id=user.id,
            qnt_room=2
            )
        
        use_case.execute(request)

        assert user.name == "Teste"
        assert user.qnt_room == 2
        mock_repository.update.assert_called_once_with(user) 

