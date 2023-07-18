from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from sqlalchemy import and_, exc, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection

from db_strikes.exception import ModelNotFoundException
from db_strikes.infra.db.schema import contents, contents_authors_association
from db_strikes.repositories.authors import Author
from db_strikes.repositories.contents import Content
from status import Status


@dataclass
class ContentAuthor:
    id: UUID
    author: Author
    content: Content
    updated_at: datetime
    created_at: datetime


def new_author_to_content(conn: Connection, content_id: UUID, author_id: UUID, content: Content, author: Author) -> ContentAuthor:
    """ Insert a new author item into the database and return the inserted auther. """

    try:
        content_author = conn.execute(insert(contents_authors_association)
                                      .values(content_id=content_id, author_id=author_id)
                                      .returning(contents_authors_association)).fetchone()

        """ Append the new author_id to the existing author_id list in the contents table """
        conn.execute(contents.update().where(contents.c.id == content_id).values(author_id=func.array_append(contents.c.author_id, author_id)))

        return ContentAuthor(id=content_author.id,
                             author=author,
                             content=content,
                             created_at=content_author.created_at,
                             updated_at=content_author.updated_at)

    except exc.SQLAlchemyError as e:
        status = Status(' FAIL: Author id ' + author_id, f', error adding author to content{e.args}', ' ')
        raise Exception(status.get_status())


def delete_author_from_content(conn: Connection, content_id: UUID, author_id: UUID) -> None:
    """ Delete author from the content. Raises: If the author id or content id not exist """
    if not conn.execute(contents_authors_association
                        .delete()
                        .where(and_(contents_authors_association.c.content_id == content_id,
                                    contents_authors_association.c.author_id == author_id))).rowcount:
        raise ModelNotFoundException('contents_authors_association', f'Association for author id {author_id} or content id {content_id}', '')

    conn.execute(contents.update().where(contents.c.id == content_id).values(author_id=func.array_remove(contents.c.author_id, author_id)))
