from uuid import uuid4
from unittest.mock import create_autospec
from src.core.room.domain.room_repository import RoomRepository

from src.core.room.domain.room import Room
from src.core.room.application.use_cases.update_room import UpdateRoom
import pytest
from src.core.room.application.use_cases.exceptions import RoomNotFound
from src.core.room.infra.in_memory_room_repository import InMemoryRoomRepository

@pytest.mark.room
class TestDeleteRoom:
    def test_update_room_from_repository(self):
        room = Room(
            name="Study Room", 
            user_id=uuid4(), 
            )

        repository = InMemoryRoomRepository(rooms=[room])

        use_case = UpdateRoom(repository=repository)
        use_case.execute(UpdateRoom.Input(id=room.id, name="Test Room"))

        updated_room = repository.get_by_id(room.id)
        assert updated_room.id == room.id
        assert updated_room.name == "Test Room"


    def test_update_room_when_room_not_found_then_raise_exception(self):

        repository = InMemoryRoomRepository()

        use_case = UpdateRoom(repository=repository)

        with pytest.raises(RoomNotFound):
            use_case.execute(UpdateRoom.Input(id=uuid4(), name="Test Room"))
        