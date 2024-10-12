from uuid import uuid4
from unittest.mock import create_autospec
from src.core.room.domain.room_repository import RoomRepository
from src.core.room.domain.room import Room
from src.core.room.application.use_cases.delete_room import DeleteRoom
import pytest
from src.core.room.application.use_cases.exceptions import RoomNotFound

@pytest.mark.room
class TestDeleteRoom:
    def test_delete_room_from_repository(self):
        room = Room(
            name="Study Room", 
            user_id=uuid4(), 
            )

        mock_repository = create_autospec(RoomRepository)
        mock_repository.get_by_id.return_value = room

        use_case = DeleteRoom(mock_repository)
        use_case.execute(DeleteRoom.Input(id=room.id))

        mock_repository.delete.assert_called_once_with(room.id)

    def test_when_room_not_found_then_raise_exception(self):
        mock_repository = create_autospec(RoomRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteRoom(mock_repository)

        with pytest.raises(RoomNotFound):
            use_case.execute(DeleteRoom.Input(id=uuid4()))
        
        mock_repository.delete.assert_not_called() 
        assert mock_repository.delete.called is False