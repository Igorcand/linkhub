from uuid import UUID
from dataclasses import dataclass
from src.core.post.domain.post import Post
from src.core.post.domain.post_repository import PostRepository
from src.core.post.application.use_cases.exceptions import PostNotFound, InvalidPostData

from src.core.link.domain.link_repository import LinkRepository
from src.core.link.application.use_cases.exceptions import RelatedLinksNotFoundForUser



class UpdatePost:

    @dataclass
    class Input:
        id: UUID
        user_id: UUID
        title: str | None = None
        body: str | None = None
        links: set[UUID] | None = None


    def __init__(self, repository: PostRepository, link_repository: LinkRepository) -> None:
        self.repository = repository
        self.link_repository = link_repository


    def execute(self, request: Input) -> None:
        post = self.repository.get_by_id(id=request.id)
        if post is None:
            raise PostNotFound(f"Post with {request.id} not found")

        current_title = post.title
        current_body = post.body
        current_links = post.links

        if request.title is not None: current_title = request.title
        
        if request.body is not None: current_body = request.body

        if request.links is not None: current_links = request.links
        

        links_ids = {link.id for link in self.link_repository.list(user_id=request.user_id)}
        if not request.links.issubset(links_ids):
            raise RelatedLinksNotFoundForUser(
                f"Links related for user not found: {request.links - links_ids}"
            )
        

        try:
            post.update_post(
                title=current_title,
                body=current_body,
                links=current_links,
                )
        except ValueError as err:
            raise InvalidPostData(err)
    
        
        self.repository.update(post)
    