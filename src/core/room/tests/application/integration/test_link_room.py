from unittest.mock import create_autospec
from src.core.room.application.use_cases.list_room import ListRoom, RoomOutput
from src.core.room.domain.room_repository import RoomRepository
from src.core.room.domain.room import Room
import pytest
from uuid import uuid4
from src.core.room.infra.in_memory_room_repository import InMemoryRoomRepository

@pytest.mark.room
class TestListRoom:
    def test_when_no_rooms_in_repository_then_return_empty_list(self):
        repository = InMemoryRoomRepository()

        use_case = ListRoom(repository=repository)
        response = use_case.execute(ListRoom.Input())

        assert response == ListRoom.Output(
            data=[]
            )
    
    def test_when_categories_in_repository_then_return_list(self):
        room = Room(
            name="Study Room", 
            user_id=uuid4(), 
        )
        repository = InMemoryRoomRepository(rooms=[room])

        use_case = ListRoom(repository=repository)
        response = use_case.execute(ListRoom.Input())

        assert response == ListRoom.Output(
            data=[
                RoomOutput(
                    id=room.id,
                    name=room.name,
                    user_id=room.user_id
                ),
            ]
        )
    