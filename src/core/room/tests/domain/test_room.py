import pytest
from uuid import UUID, uuid4
from src.core.room.domain.room import Room

@pytest.mark.room
class TestRoom:
    def test_field_is_required(self):
        with pytest.raises(TypeError):
            Room()
    
    def test_name_must_have_be_less_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            Room(user_id=uuid4(), name='a'*256)
        

    def test_cannot_create_room_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Room(user_id=uuid4(), name='')


    def test_room_is_created_with_provided_values(self):
        id = uuid4()
        user_id = uuid4()

        room = Room(
            id=id, 
            name="Study Room",
            user_id=user_id 
            )
        
        assert room.id == id
        assert room.name == "Study Room"
        assert room.user_id == user_id

