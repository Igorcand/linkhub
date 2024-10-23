from src.core.post.domain.post_repository import PostRepository
from src.django_project.room_app.models import Room as RoomORM
from src.django_project.user_app.models import User as UserORM
from src.django_project.link_app.models import Link as LinkORM
from src.django_project.post_app.models import Post as PostORM


from src.core.post.domain.post import Post
from uuid import UUID
from typing import List, Optional
from django.db import transaction

class DjangoORMPostRepository(PostRepository):
    def __init__(self, model: RoomORM | None = None) -> None:
        self.model = model or RoomORM

    def create(self, post: Post) -> None: 
        user = UserORM.objects.get(id=post.user_id) 
        room = RoomORM.objects.get(id=post.room_id)   

        post_orm= PostORM(
            id=post.id,
            title=post.title,
            body=post.body,

            user_id = user,
            room_id = room,
            )
        post_orm.links.set(post.links)
        post_orm.save()

    def get_by_id(self, id: UUID) -> Optional[Post]:
        try:
            post = self.model.objects.get(id=id)
            return PostModelMapper.to_entity(post)
        except self.model.DoesNotExist:
            return None
    
    def validate_if_user_id_has_post_in_room_id(self, user_id: UUID, room_id=UUID) -> bool:
        try:
            existe_post = PostORM.objects.filter(user_id=user_id, room_id=room_id).exists()
            return existe_post
        except self.model.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        return self.model.objects.filter(id=id).delete()

    def list_by_room_id(self, room_id: UUID) -> List[Post]:
        return [
            PostModelMapper.to_entity(room_model)
            for room_model in self.model.objects.filter(room_id=room_id)]

class PostModelMapper:
    @staticmethod
    def to_model(post: Post) -> RoomORM:
        return RoomORM(
            id=post.id,
            title=post.title,
            body=post.body,
            user_id = post.user_id,
            room_id = post.room_id,
        )
    
    def to_entity(post: PostORM) -> Post:
        return Post(
            id=post.id,
            title=post.title,
            body=post.body,
            user_id = post.user_id.id,
            room_id = post.room_id.id,
        )
    
        