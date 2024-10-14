import pytest
from uuid import UUID, uuid4
from src.core.post.domain.post import Post

@pytest.mark.room
class TestRoom:
    def test_field_is_required(self):
        with pytest.raises(TypeError):
            Post()
    
    def test_title_must_have_be_less_characters(self):
        with pytest.raises(ValueError, match="title cannot be longer than 150"):
            Post(room_id=uuid4(), user_id=uuid4(), links=[uuid4(), uuid4()], title='a'*151)
        

    def test_cannot_create_room_with_empty_name(self):
        with pytest.raises(ValueError, match="title cannot be empty"):
            Post(room_id=uuid4(), user_id=uuid4(), links=[uuid4(), uuid4()], title='')


    def test_post_is_created_with_provided_values(self):
        id = uuid4()
        user_id = uuid4()
        room_id = uuid4()
        links_ids = [uuid4(), uuid4()]


        post = Post(
            id=id, 
            room_id=room_id,
            user_id=user_id,
            links=links_ids,
            title="My Post",
            body="I would like to shere my links"
            )
        
        assert post.id == id
        assert post.room_id == room_id
        assert post.user_id == user_id
        assert post.links == links_ids
        assert post.title == "My Post"
        assert post.body == "I would like to shere my links"


