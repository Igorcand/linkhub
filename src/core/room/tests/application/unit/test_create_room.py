from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.room.application.use_cases.create_room import CreateRoom
from src.core.room.application.use_cases.exceptions import InvalidRoomData
from src.core.user.application.use_cases.exceptions import UserNotFound

from src.core.room.domain.room_repository import RoomRepository
from src.core.user.domain.user_repository import UserRepository
from src.core.user.domain.user import User


import pytest

@pytest.mark.room
class TestCreateRoom:
    def test_create_room_with_valid_data(self):
        mock_repository = MagicMock(RoomRepository)
        mock_user_repository = MagicMock(UserRepository)

        user = User(
            id=uuid4(),
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        mock_user_repository.get_by_id.return_value = user
        use_case = CreateRoom(repository=mock_repository, user_repository=mock_user_repository)
        request = CreateRoom.Input(
            name="Study Room", 
            user_id=uuid4()
            )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateRoom.Output)
        assert isinstance(response.id, UUID)
        assert mock_repository.create.called is True
    
    def test_create_room_with_no_data_provided(self):
        mock_repository = MagicMock(RoomRepository)
        mock_user_repository = MagicMock(UserRepository)

        use_case = CreateRoom(repository=mock_repository, user_repository=mock_user_repository)
        with pytest.raises(TypeError) as exc_info:
            response = use_case.execute(CreateRoom.Input())

    def test_create_room_with_invalid_data(self):
        mock_repository = MagicMock(RoomRepository)
        mock_user_repository = MagicMock(UserRepository)

        use_case = CreateRoom(repository=mock_repository, user_repository=mock_user_repository)
        with pytest.raises(InvalidRoomData, match="name cannot be empty") as exc_info:
            response = use_case.execute(CreateRoom.Input(name="", user_id=uuid4()))
    
    def test_create_room_with_user_not_existing(self):
        mock_repository = MagicMock(RoomRepository)
        mock_user_repository = MagicMock(UserRepository)
        mock_user_repository.get_by_id.return_value = None

        use_case = CreateRoom(repository=mock_repository, user_repository=mock_user_repository)
        request = CreateRoom.Input(
            name="Study Room", 
            user_id=uuid4()
            )
        with pytest.raises(UserNotFound) as exc_info:
            response = use_case.execute(request)