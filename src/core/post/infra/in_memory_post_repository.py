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
    
    def get_by_user_id(self, user_id: UUID) -> Post | None:
        for post in self.posts:
            if post.user_id == user_id:
                return post
        return None
    
    def list_by_room_id(self, room_id: UUID) -> Post | None:
        posts_by_room = []
        for post in self.posts:
            if post.room_id == room_id:
                posts_by_room.append(post)
        return posts_by_room
    
    def delete(self, id: UUID) -> None:
        post = self.get_by_id(id)
        self.posts.remove(post)
    
    def update(self, post: Post) -> None:
        old_post = self.get_by_id(post.id)
        if old_post:
            self.posts.remove(old_post)
            self.posts.append(post)
    
    def list(self) -> list[Post]:
        return [post for post in self.posts]
 