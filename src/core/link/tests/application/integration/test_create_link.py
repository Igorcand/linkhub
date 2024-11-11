from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.link.application.use_cases.create_link import CreateLink
from src.core.link.application.use_cases.exceptions import InvalidLinkData
from src.core.user.application.use_cases.exceptions import UserNotFound

from src.core.link.domain.link_repository import LinkRepository
from src.core.user.domain.user_repository import UserRepository
from src.core.user.domain.user import User

from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.link.infra.in_memory_link_repository import InMemoryLinkRepository



import pytest

@pytest.mark.link
class TestCreateLink:
    def test_create_link_with_valid_data(self):
        repository = InMemoryLinkRepository()

        user = User(
            id=uuid4(),
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        
        user_repository = InMemoryUserRepository(users=[user])
        use_case = CreateLink(repository=repository, user_repository=user_repository)
        request = CreateLink.Input(
            url="www.google.com", 
            user_id=user.id
            )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateLink.Output)
        assert isinstance(response.id, UUID)
    
    
    def test_create_link_with_user_not_existing(self):
        repository = InMemoryLinkRepository()      
        user_repository = InMemoryUserRepository()

        use_case = CreateLink(repository=repository, user_repository=user_repository)
        request = CreateLink.Input(
            url="www.google.com", 
            user_id=uuid4()
            )
        with pytest.raises(UserNotFound) as exc_info:
            
            response = use_case.execute(request)