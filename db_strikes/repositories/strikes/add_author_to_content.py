from db_strikes.controllers.models.contents_authors_associations import ContentAuthor
from db_strikes.infra.db.engine import engine
from db_strikes.repositories import contents_authors_associations
from db_strikes.repositories.strikes import add_author_to_content



class ContentAuthor:
    def add_author_to_content(content_id: UUID, author_id: UUID):
        """ Insert a new author item into the database and return the inserted auther. """
        content_info = contents.get_by_id(conn, content_id)
        author_info = authors.get_by_id(conn, author_id)

        try:
            content_author = conn.execute(insert(contents_authors_association).values(content_id=content_id, author_id=author_id)
                                        .returning(contents_authors_association)).fetchone()
            return ContentAuthor(id=content_author.id, author=author_info, content=content_info, created_at=content_author.created_at, updated_at=content_author.updated_at)
        except exc.SQLAlchemyError as e:
            return e.args