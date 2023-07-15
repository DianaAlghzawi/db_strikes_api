from dataclasses import dataclass
from datetime import datetime
from typing import Text
from uuid import UUID

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection

from db_strikes.exception import ModelNotFoundException
from db_strikes.infra.db.schema import authors


@dataclass(frozen=True)
class Author:
    id: UUID
    bio: Text
    created_at: datetime
    updated_at: datetime


def new(conn: Connection, bio: Text) -> Author:
    """ Insert a new author item into the database and return the inserted auther. """
    return Author(**(conn.execute(insert(authors).values(bio=bio).returning(authors)).fetchone())._asdict())


def get_by_id(conn: Connection, id: UUID) -> Author:
    """ Get the author by id and raise if the id not exist. """
    if author_info := conn.execute(authors.select().where(authors.c.id == id)).fetchone():
        return Author(**author_info._asdict())
    raise ModelNotFoundException('Authors', 'id', id)


def delete(conn: Connection, id: UUID) -> None:
    """ Delete author from the database. Raises: If the author id not exist """
    if not conn.execute(authors.delete().where(authors.c.id == id)).rowcount:
        raise ModelNotFoundException('Authors', 'id', id)


def update(conn: Connection, id: UUID, bio: Text) -> Author:
    """ Update author bio from the database. Raises: If the author id not exist """

    if author_info := conn.execute(authors.update().where(authors.c.id == id).values(bio=bio).returning(authors)).fetchone():
        return Author(**author_info._asdict())
    raise ModelNotFoundException('Authors', 'id', id)
