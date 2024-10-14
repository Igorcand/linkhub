from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class Post():
    room_id : UUID
    user_id: UUID
    title: str
    body: str = ""
    links : set[UUID] = field(default_factory=set)
    id: UUID = field(default_factory=uuid4)


    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if len(self.title) > 150:
            raise ValueError("title cannot be longer than 150")
        
        if not self.title:
            raise ValueError("title cannot be empty")

        if len(self.body) > 1024:
            raise ValueError("body cannot be longer than 1024")

        
    def __str__(self):
        return f"{self.title} - {self.id}"
    
    def __repr__(self) -> str:
        return f"Post {self.title} ({self.id})"

    def update_title(self, title):
        self.title = title 

        self.validate()
    
    def update_body(self, body):
        self.body = body 

        self.validate()