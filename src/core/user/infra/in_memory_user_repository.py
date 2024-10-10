from uuid import UUID
from src.core.user.domain.user import User
from src.core.user.domain.user_repository import UserRepository

class InMemoryUserRepository(UserRepository):
    def __init__(self, users=None) -> None:
        self.users = users or []
    
    def create(self, user) -> None:
        self.users.append(user)
    
    def get_by_id(self, id: UUID) -> User | None:
        for user in self.users:
            if user.id == id:
                return user
        return None
    
    def get_by_username(self, username: str) -> User | None:
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def delete(self, id: UUID) -> None:
        user = self.get_by_id(id)
        self.users.remove(user)
    
    def update(self, user: User) -> None:
        old_user = self.get_by_id(user.id)
        if old_user:
            self.users.remove(old_user)
            self.users.append(user)
    
    def list(self) -> list[User]:
        return [user for user in self.users]