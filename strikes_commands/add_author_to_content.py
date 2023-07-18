from uuid import UUID

from db_strikes.repositories import authors, contents_authors_associations
from db_strikes.repositories.contents_authors_associations import ContentAuthor
from status import Status
from strikes_commands.strikes_base import StrikesBase


class AddAuthorToContent(StrikesBase):
    def add_author_to_content(self) -> ContentAuthor:
        try:
            author = authors.get_by_id(self.conn, self.author_id)
            content_author = contents_authors_associations.new_author_to_content(
                self.conn, self.content_id, self.author_id, self.get_content(), author)
            status = Status(' SUCCESS: ', f'{self.content_id} ,', content_author)

        except Exception as e:
            status = Status('FAIL: Content id ' + self.content_id, f', error adding author to content{e.args[0]}', '')

        return status.get_status()

    def delpoy_changes(self, author_id: UUID):
        self.author_id = author_id
        return self.add_author_to_content()


input_file = open('strikes_input/add_author_to_content.csv')

for ids in input_file.readlines():
    author_id, content_id = ids.split(',')
    obj = AddAuthorToContent(content_id[:-1])
    print(obj.delpoy_changes(author_id))
