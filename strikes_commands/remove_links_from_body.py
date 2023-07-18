import re

from db_strikes.repositories.contents import Content
from db_strikes.services import contents
from status import Status
from strikes_commands.strikes_base import StrikesBase


class RemoveLinksFromBody(StrikesBase):
    def remove_links_from_body(self) -> Content:
        try:
            content = contents.get_by_id(self.content_id)
            regex_equation = r'https?://(\w+/)+\w*\s'
            content.body = re.sub(regex_equation, '', content.body)
            content = contents.update(self.content_id, content)
            status = Status('Successfully ', 'Content body links has been Successfully removed', f' {content}')
        except Exception as e:
            status = Status(f'Fail: error removing links from content{e.args}', f', {self.content_id} ', 'not exist')

        return status.get_status()

    def delpoy_changes(self):
        return self.remove_links_from_body()


content_ids = open('strikes_input/remove_links_from_body.csv')
for content_id in content_ids.readlines():
    obj = RemoveLinksFromBody(content_id[:-1])
    print(obj.delpoy_changes())
