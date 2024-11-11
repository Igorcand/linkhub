from src.core.room.domain.room_repository import RoomRepository
from src.django_project.room_app.models import Room as RoomORM
from src.django_project.user_app.models import User as UserORM

from src.core.room.domain.room import Room
from uuid import UUID
from typing import List, Optional
from django.db import transaction

class DjangoORMRoomRepository(RoomRepository):
    def __init__(self, model: RoomORM | None = None) -> None:
        self.model = model or RoomORM

    def create(self, room: Room) -> None: 
        user = UserORM.objects.get(id=room.user_id)   
        room_orm= RoomORM(
            id=room.id,
            name=room.name,
            user_id = user,
            )
        room_orm.save()

    def get_by_id(self, id: UUID) -> Optional[Room]:
        try:
            room = self.model.objects.get(id=id)
            return RoomModelMapper.to_entity(room)
        except self.model.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        return self.model.objects.filter(id=id).delete()

    def update(self, room: Room) -> None:
        self.model.objects.filter(pk=room.id).update(
            name=room.name,
        )

    def list(self) -> List[Room]:
        return [
            RoomModelMapper.to_entity(room_model)
            for room_model in self.model.objects.all()]

class RoomModelMapper:
    @staticmethod
    def to_model(room: Room) -> RoomORM:
        return RoomORM(
            id=room.id,
            name=room.name,
            user_id = room.user_id,

        )
    
    def to_entity(room: RoomORM) -> Room:
        return Room(
            id=room.id,
            name=room.name,
            user_id = room.user_id.id,
        )