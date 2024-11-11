from src.core.user.domain.user_repository import UserRepository
from src.django_project.user_app.models import User as UserORM
from src.core.user.domain.user import User
from uuid import UUID
from typing import List, Optional
from django.db import transaction

class DjangoORMUserRepository(UserRepository):
    def __init__(self, model: UserORM | None = None) -> None:
        self.model = model or UserORM

    def create(self, user: User) -> User:
        if UserORM.objects.filter(email=user.email).exists():
            raise ValueError(f"User with the email {user.email} already exists")
    
        user_orm= UserORM(
            id=user.id,
            name=user.name,
            username = user.username,
            email=user.email,
            password=user.password
            )
        user_orm.set_password(user.password)
        user_orm.save()

    def get_by_id(self, id: UUID) -> Optional[User]:
        try:
            user = self.model.objects.get(id=id)
            return UserModelMapper.to_entity(user)
        except self.model.DoesNotExist:
            return None

    def get_by_username(self, username: str) -> Optional[User]:
        return UserORM.objects.filter(username=username).first()

    def delete(self, id: UUID) -> None:
        return self.model.objects.filter(id=id).delete()

    def update(self, user: User) -> None:
        self.model.objects.filter(pk=user.id).update(
            username=user.username,
            qnt_room=user.qnt_room,

        )

    def list(self) -> List[User]:
        return [
            UserModelMapper.to_entity(user_model)
            for user_model in self.model.objects.all()]

class UserModelMapper:
    @staticmethod
    def to_model(user: User) -> UserORM:
        return UserORM(
            id=user.id,
            name=user.name,
            username = user.username,
            email=user.email,
            password=user.password,
            qnt_room=user.qnt_room

        )
    
    def to_entity(user: UserORM) -> User:
        return User(
            id=user.id,
            name=user.name,
            username = user.username,
            email=user.email,
            password=user.password,
            qnt_room=user.qnt_room
        )