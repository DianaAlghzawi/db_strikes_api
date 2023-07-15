from dataclasses import dataclass
from datetime import datetime
from typing import Text
from uuid import UUID

from sqlalchemy import exc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection

from db_strikes.exception import ModelNotFoundException
from db_strikes.infra.db.schema import contents_authors_association
from db_strikes.repositories import authors, contents


@dataclass()
class ContentAuthor:
    id: UUID
    author: authors.Author
    content: contents.Content
    updated_at: datetime
    created_at: datetime

    def __init__(self, id: UUID, author: authors.Author, content: contents.Content, created_at: datetime, updated_at: datetime):
        self.id = id
        self.author = author
        self.content = content
        self.updated_at = updated_at
        self.created_at = created_at


def new(conn: Connection, content_id: UUID, author_id: UUID):
    """ Insert a new author item into the database and return the inserted auther. """
    content_info = contents.get_by_id(conn, content_id)
    author_info = authors.get_by_id(conn, author_id)

    try:
        content_author = conn.execute(insert(contents_authors_association).values(content_id=content_id, author_id=author_id)
                                      .returning(contents_authors_association)).fetchone()
        return ContentAuthor(id=content_author.id, author=author_info, content=content_info, created_at=content_author.created_at, updated_at=content_author.updated_at)
    except exc.SQLAlchemyError as e:
        return e.args


# def get_by_id(conn: Connection, id: UUID) -> Author:
#     """ Get the author by id and raise if the id not exist. """
#     if author_info := conn.execute(authors.select().where(authors.c.id == id)).fetchone():
#         return Author(**author_info._asdict())
#     raise ModelNotFoundException('Authors', 'id', id)


# def delete(conn: Connection, id: UUID) -> None:
#     """ Delete author from the database. Raises: If the author id not exist """
#     if not conn.execute(authors.delete().where(authors.c.id == id)).rowcount:
#         raise ModelNotFoundException('Authors', 'id', id)


# def update(conn: Connection, id: UUID, bio: Text) -> Author:
#     """ Update author bio from the database. Raises: If the author id not exist """

#     if author_info := conn.execute(authors.update().where(authors.c.id == id).values(bio=bio).returning(authors)).fetchone():
#         return Author(**author_info._asdict())
#     raise ModelNotFoundException('Authors', 'id', id)
