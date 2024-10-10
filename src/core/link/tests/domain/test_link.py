import pytest
from uuid import UUID, uuid4
from src.core.link.domain.link import Link

@pytest.mark.link
class TestUser:
    def test_field_is_required(self):
        with pytest.raises(TypeError):
            Link()
    
    def test_url_must_have_be_less_characters(self):
        with pytest.raises(ValueError, match="url cannot be longer than 255"):
            Link(user_id=uuid4(), url='a'*256)
        

    def test_cannot_create_link_with_empty_url(self):
        with pytest.raises(ValueError, match="url cannot be empty"):
            Link(user_id=uuid4(), url='')


    def test_user_is_created_with_provided_values(self):
        id = uuid4()
        user_id = uuid4()

        user = Link(
            id=id, 
            url="www.google.com",
            user_id=user_id 
            )
        
        assert user.id == id
        assert user.url == "www.google.com"
        assert user.user_id == user_id

