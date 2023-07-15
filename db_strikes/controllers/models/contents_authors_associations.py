from uuid import UUID

from pydantic import BaseModel


class ContentAuthor(BaseModel):
    content_id: UUID
    author_id: UUID
