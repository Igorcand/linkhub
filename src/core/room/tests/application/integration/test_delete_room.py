from uuid import uuid4
from unittest.mock import create_autospec
from src.core.room.domain.room_repository import RoomRepository
from src.core.room.domain.room import Room
from src.core.room.application.use_cases.delete_room import DeleteRoom
import pytest
from src.core.room.application.use_cases.exceptions import RoomNotFound
from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.room.infra.in_memory_room_repository import InMemoryRoomRepository

@pytest.mark.room
class TestDeleteRoom:
    def test_delete_room_from_repository(self):
        room = Room(
            name="Study Room", 
            user_id=uuid4(), 
        )
        repository = InMemoryRoomRepository(rooms=[room])

        use_case = DeleteRoom(repository=repository)
        request = use_case.execute(DeleteRoom.Input(id=room.id))

        assert repository.get_by_id(room.id) is None
        assert request is None

    def test_when_room_not_found_then_raise_exception(self):
        repository = InMemoryRoomRepository()

        use_case = DeleteRoom(repository)

        with pytest.raises(RoomNotFound):
            use_case.execute(DeleteRoom.Input(id=uuid4()))
        