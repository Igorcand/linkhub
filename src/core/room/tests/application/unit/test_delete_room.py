from uuid import uuid4
from unittest.mock import create_autospec
from src.core.room.domain.room_repository import RoomRepository
from src.core.user.domain.user_repository import UserRepository

from src.core.room.domain.room import Room
from src.core.room.application.use_cases.delete_room import DeleteRoom
import pytest
from src.core.room.application.use_cases.exceptions import RoomNotFound
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

        mock_user_repository = create_autospec(UserRepository)
        mock_user_repository.get_by_id.return_value = user

        room = Room(
            name="Study Room", 
            user_id=uuid4(), 
            )

        mock_repository = create_autospec(RoomRepository)
        mock_repository.get_by_id.return_value = room

        use_case = DeleteRoom(repository=mock_repository, user_repository=mock_user_repository)
        use_case.execute(DeleteRoom.Input(id=room.id, user_id=user.id))

        mock_repository.delete.assert_called_once_with(room.id)

    def test_when_room_not_found_then_raise_exception(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*',
            )

        mock_user_repository = create_autospec(UserRepository)
        mock_user_repository.get_by_id.return_value = user

        mock_repository = create_autospec(RoomRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteRoom(repository=mock_repository, user_repository=mock_user_repository)

        with pytest.raises(RoomNotFound):
            use_case.execute(DeleteRoom.Input(id=uuid4(), user_id=user.id))
        
        mock_repository.delete.assert_not_called() 
        assert mock_repository.delete.called is False