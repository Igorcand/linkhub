from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.room.application.use_cases.create_room import CreateRoom
from src.core.room.application.use_cases.exceptions import InvalidRoomData
from src.core.user.application.use_cases.exceptions import UserNotFound

from src.core.room.domain.room_repository import RoomRepository
from src.core.user.domain.user_repository import UserRepository
from src.core.user.domain.user import User

from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.room.infra.in_memory_room_repository import InMemoryRoomRepository



import pytest

@pytest.mark.room
class TestCreateRoom:
    def test_create_room_with_valid_data(self):
        repository = InMemoryRoomRepository()

        user = User(
            id=uuid4(),
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        
        user_repository = InMemoryUserRepository(users=[user])
        use_case = CreateRoom(repository=repository, user_repository=user_repository)
        request = CreateRoom.Input(
            name="Study Room", 
            user_id=user.id
            )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateRoom.Output)
        assert isinstance(response.id, UUID)
    
    
    def test_create_room_with_user_not_existing(self):
        repository = InMemoryRoomRepository()      
        user_repository = InMemoryUserRepository()

        use_case = CreateRoom(repository=repository, user_repository=user_repository)
        request = CreateRoom.Input(
            name="Study Room", 
            user_id=uuid4()
            )
        with pytest.raises(UserNotFound) as exc_info:
            response = use_case.execute(request)