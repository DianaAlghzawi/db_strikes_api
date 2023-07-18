from typing import Optional
from uuid import UUID

from db_strikes.infra.db.engine import engine
from db_strikes.services import authors, contents


class ContentAuthorAssociationManager():
    def __init__(self, author_id: Optional[UUID] = None, content_id: Optional[UUID] = None):
        self.conn = engine.connect()
        self.author_id = author_id
        self.content_id = content_id

    def get_author(self) -> authors.Author:
        return authors.get_author_by_id(self.author_id)

    def get_content(self) -> contents.Content:
        return contents.get_content_by_id(self.content_id)

    def update_content(self, content) -> contents.Content:
        return contents.update_content(self.content_id, content)
