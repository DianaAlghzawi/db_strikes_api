from typing import Text
from uuid import UUID

from db_strikes.controllers.models.contents import PatchContents
from db_strikes.infra.db.engine import engine
from db_strikes.repositories import contents
from db_strikes.repositories.contents import Content


def new_content(body: Text, status: str) -> Content:
    with engine.begin() as conn:
        return contents.new(conn, body, status)


def get_content_by_id(id: UUID) -> Content:
    with engine.connect() as conn:
        return contents.get_by_id(conn, id)


def delete_content(id: UUID) -> None:
    with engine.begin() as conn:
        return contents.delete(conn, id)


def update_content(id: UUID, content: PatchContents) -> Content:
    with engine.begin() as conn:
        return contents.update(conn, id, content)
