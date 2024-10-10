import pytest
from uuid import UUID, uuid4
from src.core.user.domain.user import User

@pytest.mark.user
class TestUser:
    def test_field_is_required(self):
        with pytest.raises(TypeError):
            User()
    
    def test_field_must_have_be_less_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            User(name="a"*256, username='usertest', email='test@ulife.com.br', password='123test*')
        
        with pytest.raises(ValueError, match="username cannot be longer than 30"):
            User(name="testando", username="a"*31, email='test@ulife.com.br', password='123test*')

    def test_cannot_create_user_with_empty_fields(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            User(name="", username='usertest', email='test@ulife.com.br', password='123test*')

        with pytest.raises(ValueError, match="username cannot be empty"):
            User(name="Test", username='', email='test@ulife.com.br', password='123test*')
        
        with pytest.raises(ValueError, match="email cannot be empty"):
            User(name="Test", username='usertest', email='', password='123test*')
        
        with pytest.raises(ValueError, match="password cannot be empty"):
            User(name="Test", username='usertest', email='test@ulife.com.br', password='')
    
    def test_cannot_create_user_with_email_not_from_ulife(self):
        with pytest.raises(ValueError, match="invalid email format"):
            User(name="teste", username='usertest', email='test@gmail.com', password='123test*')

    def test_user_is_created_with_provided_values(self):
        id = uuid4()
        user = User(
            id=id, 
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        
        assert user.id == id
        assert user.name == "Teste"
        assert user.username == "Teste123"
        assert user.email == "test@ulife.com.br"
        assert user.password == "123test*"



@pytest.mark.user
class TestUpdateQntRoom():
    def test_update_qnt_room(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        user.update_qnt_room(1)
        assert user.qnt_room == 1
    
    def test_when_qnt_room_is_lower_than_0(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        with pytest.raises(ValueError, match="qnt_room cannot be lower than 0"):
            user.update_qnt_room(-1)
    
    def test_when_qnt_room_is_bigger_than_5(self):
        user = User(
            name="Teste", 
            username="Teste123", 
            email="test@ulife.com.br", 
            password='123test*', 
            )
        with pytest.raises(ValueError, match="qnt_room cannot be bigger than 5"):
            user.update_qnt_room(6)

