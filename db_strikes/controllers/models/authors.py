from typing import Text

from pydantic import BaseModel, Field


class Author(BaseModel):
    bio: Text = Field(min_length=10)


class PatchAuthor(BaseModel):
    bio: Text = Field(min_length=10)
