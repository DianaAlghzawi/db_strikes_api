from uuid import UUID

from db_strikes.repositories import contents_authors_associations
from db_strikes.repositories.contents_authors_associations import ContentAuthor
from db_strikes.services.contents_authors_association_manager import ContentAuthorAssociationManager


class NewAuthorToContent(ContentAuthorAssociationManager):
    def __init__(self, author_id: UUID, content_id: UUID):
        super().__init__(content_id, author_id)

    def add_author_to_content(self) -> ContentAuthor:
        """ Insert a new author item into the database and return the inserted auther. """
        content = self.get_content()
        author = self.get_author()

        return contents_authors_associations.new_author_to_content(self.conn, self.content_id, self.author_id, content, author)
