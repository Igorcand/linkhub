from unittest.mock import create_autospec
from src.core.room.application.use_cases.list_room import ListRoom, RoomOutput
from src.core.room.domain.room_repository import RoomRepository
from src.core.room.domain.room import Room
import pytest
from uuid import uuid4

@pytest.mark.room
class TestListRoom:
    def test_when_no_rooms_in_repository_then_return_empty_list(self):
        mock_repository = create_autospec(RoomRepository)
        mock_repository.list.return_value = []

        use_case = ListRoom(repository=mock_repository)
        response = use_case.execute(ListRoom.Input())

        assert response == ListRoom.Output(
            data=[]
            )
    
    def test_when_categories_in_repository_then_return_list(self):
        room = Room(
            name="Study Room", 
            user_id=uuid4(), 
        )
        mock_repository = create_autospec(RoomRepository)
        mock_repository.list.return_value = [room]

        use_case = ListRoom(repository=mock_repository)
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
    