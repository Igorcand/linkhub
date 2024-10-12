from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class Room():
    user_id : UUID
    name : str
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if not self.name:
            raise ValueError("name cannot be empty")
        
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255")

    def __str__(self):
        return f"{self.name} - {self.user_id}"
    
    def __repr__(self) -> str:
        return f"Room ({self.id})"

