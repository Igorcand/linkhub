from uuid import uuid4
from unittest.mock import create_autospec
from src.core.user.domain.user_repository import UserRepository
from src.core.user.domain.user import User
from src.core.user.application.use_cases.delete_user import DeleteUser
from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
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

        repository = InMemoryUserRepository(users=[user])

        use_case = DeleteUser(repository)
        request = use_case.execute(DeleteUser.Input(id=user.id))

        assert repository.get_by_id(user.id) is None
        assert request is None
