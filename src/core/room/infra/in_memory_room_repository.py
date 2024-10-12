from uuid import UUID
from src.core.room.domain.room import Room
from src.core.room.domain.room_repository import RoomRepository

class InMemoryRoomRepository(RoomRepository):
    def __init__(self, rooms=None) -> None:
        self.rooms = rooms or []
    
    def create(self, room) -> None:
        self.rooms.append(room)
    
    def get_by_id(self, id: UUID) -> Room | None:
        for room in self.rooms:
            if room.id == id:
                return room
        return None
    
    def delete(self, id: UUID) -> None:
        room = self.get_by_id(id)
        self.rooms.remove(room)
    
    def update(self, room: Room) -> None:
        old_room = self.get_by_id(room.id)
        if old_room:
            self.rooms.remove(old_room)
            self.rooms.append(room)
    
    def list(self) -> list[Room]:
        return [room for room in self.rooms]
 