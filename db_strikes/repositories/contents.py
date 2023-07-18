from dataclasses import dataclass
from datetime import datetime
from typing import Text
from uuid import UUID

from sqlalchemy import exc, select
from sqlalchemy.dialects.postgresql import array, insert
from sqlalchemy.engine import Connection

from db_strikes.exception import ModelNotFoundException
from db_strikes.infra.db.enumerations import StatusEnum
from db_strikes.infra.db.schema import authors, contents


@dataclass()
class Content:
    id: UUID
    body: Text
    status: StatusEnum
    author_id: list[UUID]
    created_at: datetime
    updated_at: datetime


def get_by_id(conn: Connection, id: UUID) -> Content:
    """ Get the content by id and raise if the id not exist. """
    if author_info := conn.execute(contents.select().where(contents.c.id == id)).fetchone():
        return Content(**author_info._asdict())
    raise ModelNotFoundException('Contents', 'id', id)


def delete(conn: Connection, id: UUID) -> None:
    """ Delete content from the database. Raises: If the content id not exist """
    if not conn.execute(contents.delete().where(contents.c.id == id)).rowcount:
        raise ModelNotFoundException('Contents', 'id', id)


def new(conn: Connection, body: Text, status: str, author_id: list[UUID]) -> Content:
    """Insert a new content item into the database and return the inserted content,
    raising an exception if any author ID does not exist."""

    try:
        if author_id:
            existing_author_ids = conn.execute(select(authors.c.id).where(authors.c.id.in_(author_id))).scalars().fetchall()
            if missing_author_ids := set(author_id) - set(existing_author_ids):
                raise ModelNotFoundException('Content', 'author_id', f"Author IDs not exist in the author table: {missing_author_ids}")

        return Content(**(conn.execute(insert(contents).values(
            body=body,
            status=status,
            author_id=array(set(author_id)) if author_id else []
        ).returning(contents)).fetchone())._asdict())

    except exc.SQLAlchemyError as e:
        return Exception(e.args)


def update(conn: Connection, id: UUID, content: Content) -> Content:
    """ Update content body and status from the database. Raises: If the content id not exist """
    if author_info := conn.execute(contents.update()
                                   .where(contents.c.id == id)
                                   .values(body=content.body, status=content.status)
                                   .returning(contents)).fetchone():
        return Content(**author_info._asdict())
