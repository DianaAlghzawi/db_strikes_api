import re

from db_strikes.services.contents_authors_association_manager import ContentAuthorAssociationManager


class RemoveLinksFromBody(ContentAuthorAssociationManager):
    def __init__(self, content_id):
        super().__init__(content_id=content_id)

    def remove_links_from_body(self):
        content = self.get_content()
        regex_equation = r'http://(\w+/)+\w*\s'
        content.body = re.sub(regex_equation, '', content.body)
        self.update_content(content)
        return content
