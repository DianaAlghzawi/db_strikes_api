from typing import Optional, Text

from pydantic import BaseModel, Field

from db_strikes.infra.db.enumerations import StatusEnum


class Contents(BaseModel):
    body: Text = Field(min_length=10)
    status: StatusEnum


class PatchContents(BaseModel):
    body: Optional[Text] = Field(min_length=10)
    status: Optional[StatusEnum]
