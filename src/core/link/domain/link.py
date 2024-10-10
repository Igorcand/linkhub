from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class Link():
    user_id : UUID
    url : str
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if not self.url:
            raise ValueError("url cannot be empty")
        
        if len(self.url) > 255:
            raise ValueError("url cannot be longer than 255")
        
    
    def __str__(self):
        return f"{self.url} - {self.user_id}"
    
    def __repr__(self) -> str:
        return f"Link ({self.id})"

