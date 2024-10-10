from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class User():
    name : str
    username: str
    email: str
    password: str
    qnt_room : int = 0
    id: UUID = field(default_factory=uuid4)


    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255")
        
        if len(self.username) > 30:
            raise ValueError("username cannot be longer than 30")

        if not self.name:
            raise ValueError("name cannot be empty")
        
        if not self.username:
            raise ValueError("username cannot be empty")
        
        if not self.email:
            raise ValueError("email cannot be empty")
        
        if not "@ulife.com.br" in self.email:
            raise ValueError("invalid email format")
        
        if not self.password:
            raise ValueError("password cannot be empty")
        
        if self.qnt_room < 0:
            raise ValueError("qnt_room cannot be lower than 0")
        
        if self.qnt_room > 5:
            raise ValueError("qnt_room cannot be bigger than 5")
        
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    def __repr__(self) -> str:
        return f"User {self.name} ({self.id})"

    def update_qnt_room(self, qnt_room):
        self.qnt_room = qnt_room 

        self.validate()