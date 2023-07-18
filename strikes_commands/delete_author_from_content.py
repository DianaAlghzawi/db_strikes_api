from db_strikes.repositories import contents_authors_associations
from status import Status
from strikes_commands.strikes_base import StrikesBase
from uuid import UUID


class DeleteAuthorFromContent(StrikesBase):
    def delete_author_from_content(self) -> str:
        """ Delete author from the content """
        try:
            contents_authors_associations.delete_author_from_content(self.conn, self.content_id, self.author_id)
            status = Status('SUCCESS: Author id ' + self.author_id, ' Successfully deleted from content id:', self.content_id)
        except Exception as e:
            status = Status('FAIL: Content id ' + self.content_id, f' ,error deleting author from content{e.args}', '')

        return status.get_status()

    def delpoy_changes(self, author_id: UUID) -> str:
        """ Deploys changes by deleting the specified author from content. """
        self.author_id = author_id
        return self.delete_author_from_content()


input_file = open('strikes_input/delete_author_from_content.csv')

for ids in input_file.readlines():
    author_id, content_id = ids.split(',')
    obj = DeleteAuthorFromContent(content_id[:-1])
    print(obj.delpoy_changes(author_id))
