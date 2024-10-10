from unittest.mock import create_autospec
from uuid import uuid4
from src.core.user.application.use_cases.update_user import UpdateUser
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
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
        repository = InMemoryUserRepository(users=[user])

        use_case = UpdateUser(repository=repository)
        request = UpdateUser.Input(
            id=user.id,
            username="Teste2"
            )
        
        use_case.execute(request)

        updated_user = repository.get_by_id(user.id)

        assert updated_user.username == "Teste2"
        assert updated_user.name == "Teste"

    def test_update_qnt_room(self):
        user = User(
            id=uuid4(),
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        repository = InMemoryUserRepository(users=[user])

        use_case = UpdateUser(repository=repository)
        request = UpdateUser.Input(
            id=user.id,
            qnt_room=2
            )
        
        use_case.execute(request)

        updated_user = repository.get_by_id(user.id)

        assert updated_user.name == "Teste"
        assert updated_user.qnt_room == 2

