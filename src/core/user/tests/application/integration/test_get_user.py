from uuid import uuid4
from src.core.user.application.use_cases.get_user import GetUser
from src.core.user.domain.user import User
from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.user.application.use_cases.exceptions import UserNotFound
import pytest

@pytest.mark.user
class TestGetUser:
    def test_get_user_by_id(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        repository = InMemoryUserRepository(users=[user])
        use_case = GetUser(repository=repository)

        request = GetUser.Input(
            id=user.id)

        response = use_case.execute(request)

        assert response == GetUser.Output(
            id=user.id,
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            qnt_room=0

        )
    
    def test_when_user_does_not_exist_then_raise_exception(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        repository = InMemoryUserRepository(users=[user])
        use_case = GetUser(repository=repository)

        not_found_id = uuid4()
        request = GetUser.Input(id=not_found_id)

        with pytest.raises(UserNotFound) as exc:
            use_case.execute(request)