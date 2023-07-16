from typing import Text
from uuid import UUID

from db_strikes.infra.db.engine import engine
from db_strikes.repositories import authors
from db_strikes.repositories.authors import Author


def new_author(bio: Text) -> Author:
    with engine.begin() as conn:
        return authors.new(conn, bio)


def get_author_by_id(id: UUID) -> Author:
    with engine.connect() as conn:
        return authors.get_by_id(conn, id)


def delete_author(id: UUID) -> None:
    with engine.begin() as conn:
        return authors.delete(conn, id)


def update_author(id: UUID, bio: Text) -> Author:
    with engine.begin() as conn:
        return authors.update(conn, id, bio)
