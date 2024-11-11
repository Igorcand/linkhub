from uuid import UUID
from src.core.user.application.use_cases.create_user import CreateUser
from src.core.user.application.use_cases.exceptions import InvalidUserData
from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
import pytest

@pytest.mark.user
class TestCreateUser:
    def test_create_user_with_valid_data(self):
        repository = InMemoryUserRepository()
        use_case = CreateUser(repository=repository)

        request = CreateUser.Input(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*')

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateUser.Output)
        assert isinstance(response.id, UUID)
        
        persisted_user = repository.users[0]

        assert persisted_user.id == response.id
        assert persisted_user.name == "Teste"
        assert persisted_user.username == "Teste123"
        assert persisted_user.email == "test@ulife.com.br"
        assert persisted_user.password == '123test*'

    
    def test_create_user_with_invalid_data(self):
        repository = InMemoryUserRepository()
        use_case = CreateUser(repository=repository)

        with pytest.raises(InvalidUserData, match="name cannot be empty") as exc_info:
            response = use_case.execute(CreateUser.Input(name="", username="Teste123", email="test@ulife.com.br", password='123test*'))

        assert exc_info.type is InvalidUserData
        assert str(exc_info.value) == "name cannot be empty"

        assert len(repository.users) == 0
    