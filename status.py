from uuid import UUID


class Status:
    def __init__(self, status: str, content_id: UUID, message: str):
        self.status = status
        self.content_id = content_id
        self.message = message

    def get_status(self):
        return f'{self.status}' + f'{self.content_id}' + f'{self.message}'
