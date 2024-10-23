from uuid import UUID
from src.core.post.domain.post import Post
from src.core.post.domain.post_repository import PostRepository

class InMemoryPostRepository(PostRepository):
    def __init__(self, posts=None) -> None:
        self.posts = posts or []
    
    def create(self, post) -> None:
        self.posts.append(post)
    
    def get_by_id(self, id: UUID) -> Post | None:
        for post in self.posts:
            if post.id == id:
                return post
        return None
    
    def validate_if_user_id_has_post_in_room_id(self, user_id: UUID, room_id: UUID) -> Post | None:
        for post in self.posts:
            if post.user_id == user_id and post.room_id == room_id:
                return True
        return False
    
    def list_by_room_id(self, room_id: UUID) -> Post | None:
        posts_by_room = []
        for post in self.posts:
            if post.room_id == room_id:
                posts_by_room.append(post)
        return posts_by_room
    
    def delete(self, id: UUID) -> None:
        post = self.get_by_id(id)
        self.posts.remove(post)
    

 