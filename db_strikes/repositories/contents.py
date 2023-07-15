from dataclasses import dataclass
from datetime import datetime
from typing import Text
from uuid import UUID

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection

from db_strikes.exception import ModelNotFoundException
from db_strikes.infra.db.enumerations import StatusEnum
from db_strikes.infra.db.schema import contents


@dataclass()
class Content:
    id: UUID
    body: Text
    status: StatusEnum
    created_at: datetime
    updated_at: datetime


def new(conn: Connection, body: Text, status: str) -> Content:
    """ Insert a new content item into the database and return the inserted content. """
    return Content(**(conn.execute(insert(contents).values(body=body, status=status).returning(contents)).fetchone())._asdict())


def get_by_id(conn: Connection, id: UUID) -> Content:
    """ Get the content by id and raise if the id not exist. """
    if author_info := conn.execute(contents.select().where(contents.c.id == id)).fetchone():
        return Content(**author_info._asdict())
    raise ModelNotFoundException('Contents', 'id', id)


def delete(conn: Connection, id: UUID) -> None:
    """ Delete content from the database. Raises: If the content id not exist """
    if not conn.execute(contents.delete().where(contents.c.id == id)).rowcount:
        raise ModelNotFoundException('Contents', 'id', id)


def update(conn: Connection, id: UUID, content: Content) -> Content:
    """ Update content body from the database. Raises: If the author id not exist """
    if author_info := conn.execute(contents.update()
                                   .where(contents.c.id == id)
                                   .values(body=content.body, status=content.status)
                                   .returning(contents)).fetchone():
        return Content(**author_info._asdict())
