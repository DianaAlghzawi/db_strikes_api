from uuid import UUID

from db_strikes.repositories import contents_authors_associations
from db_strikes.repositories.contents_authors_associations import ContentAuthor
from db_strikes.services.contents_authors_association_manager import ContentAuthorAssociationManager


class DeleteAuthorFromContent(ContentAuthorAssociationManager):
    def __init__(self, author_id: UUID, content_id: UUID):
        super().__init__(content_id, author_id)

    def delete_author_from_content(self) -> ContentAuthor:
        """ Delete author item from the database """
        self.get_content()
        self.get_author()
        return contents_authors_associations.delete_author_from_content(self.conn, self.content_id, self.author_id)
