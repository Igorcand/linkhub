from uuid import uuid4
from unittest.mock import create_autospec
from src.core.room.domain.room_repository import RoomRepository
from src.core.user.domain.user_repository import UserRepository

from src.core.room.domain.room import Room
from src.core.room.application.use_cases.update_room import UpdateRoom
import pytest
from src.core.room.application.use_cases.exceptions import RoomNotFound
from src.core.user.domain.user import User

@pytest.mark.room
class TestDeleteRoom:
    def test_update_room_from_repository(self):
        room = Room(
            name="Study Room", 
            user_id=uuid4(), 
            )

        mock_repository = create_autospec(RoomRepository)
        mock_repository.get_by_id.return_value = room

        use_case = UpdateRoom(repository=mock_repository)
        use_case.execute(UpdateRoom.Input(id=room.id, name="Test Room"))

        mock_repository.update.assert_called_once_with(room)

    def test_update_room_when_room_not_found_then_raise_exception(self):

        mock_repository = create_autospec(RoomRepository)
        mock_repository.get_by_id.return_value = None

        use_case = UpdateRoom(repository=mock_repository)

        with pytest.raises(RoomNotFound):
            use_case.execute(UpdateRoom.Input(id=uuid4(), name="Test Room"))
        
        mock_repository.update.assert_not_called() 
        assert mock_repository.update.called is False