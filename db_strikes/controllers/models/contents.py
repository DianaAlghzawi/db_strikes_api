from typing import Optional, Text
from uuid import UUID

from pydantic import BaseModel, Field

from db_strikes.infra.db.enumerations import StatusEnum


class Content(BaseModel):
    body: Text = Field(min_length=10)
    status: StatusEnum
    author_id: Optional[list[UUID]] = None


class PatchContents(BaseModel):
    body: Optional[Text] = Field(min_length=10)
    status: Optional[StatusEnum]
