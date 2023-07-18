from uuid import UUID

from db_strikes.infra.db.engine import engine
from db_strikes.services import contents


class StrikesBase:
    def __init__(self, content_id: UUID):
        self.content_id = content_id
        self.conn = engine.connect()

    def get_content(self) -> contents.Content:
        return contents.get_by_id(self.content_id)

    def delpoy_changes(self) -> None:
        pass
