from uuid import uuid4
from unittest.mock import create_autospec
from src.core.room.domain.room_repository import RoomRepository
from src.core.room.domain.room import Room
from src.core.room.application.use_cases.delete_room import DeleteRoom
import pytest
from src.core.room.application.use_cases.exceptions import RoomNotFound, RoomInsufficient
from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.room.infra.in_memory_room_repository import InMemoryRoomRepository
from src.core.user.domain.user import User

@pytest.mark.room
class TestDeleteRoom:
    def test_delete_room_from_repository(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            qnt_room=3
            )
        user_repository = InMemoryUserRepository(users=[user])

        room = Room(
            name="Study Room", 
            user_id=user.id, 
        )
        repository = InMemoryRoomRepository(rooms=[room])

        use_case = DeleteRoom(repository=repository, user_repository=user_repository)
        request = use_case.execute(DeleteRoom.Input(id=room.id, user_id=user.id))

        assert repository.get_by_id(room.id) is None
        assert request is None

    def test_when_room_not_found_then_raise_exception(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        user_repository = InMemoryUserRepository(users=[user])
        repository = InMemoryRoomRepository()

        use_case = DeleteRoom(repository=repository, user_repository=user_repository)

        with pytest.raises(RoomNotFound):
            use_case.execute(DeleteRoom.Input(id=uuid4(), user_id=user.id))
    
    def test_delete_room_with_qnt_room_less_than_0_should_error(self):

        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            qnt_room=0
            )
        user_repository = InMemoryUserRepository(users=[user])

        room = Room(
            name="Study Room", 
            user_id=user.id, 
        )
        repository = InMemoryRoomRepository(rooms=[room])

        use_case = DeleteRoom(repository=repository, user_repository=user_repository)
        with pytest.raises(RoomInsufficient, match="qnt_room cannot be lower than 0"):
            use_case.execute(DeleteRoom.Input(id=room.id, user_id=user.id))

