from uuid import uuid4
from unittest.mock import create_autospec
from src.core.user.domain.user_repository import UserRepository
from src.core.user.domain.user import User
from src.core.user.application.use_cases.delete_user import DeleteUser
import pytest
from src.core.user.application.use_cases.exceptions import UserNotFound

@pytest.mark.user
class TestDeleteUser:
    def test_delete_user_from_repository(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )

        mock_repository = create_autospec(UserRepository)
        mock_repository.get_by_id.return_value = user

        use_case = DeleteUser(mock_repository)
        use_case.execute(DeleteUser.Input(id=user.id))

        mock_repository.delete.assert_called_once_with(user.id)

    def test_when_user_not_found_then_raise_exception(self):
        mock_repository = create_autospec(UserRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteUser(mock_repository)

        with pytest.raises(UserNotFound):
            use_case.execute(DeleteUser.Input(id=uuid4()))
        
        mock_repository.delete.assert_not_called() 
        assert mock_repository.delete.called is False