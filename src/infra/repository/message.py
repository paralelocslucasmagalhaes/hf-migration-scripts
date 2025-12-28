from infra.db.base_async import AsyncFirestoreCRUD
from domain.entities.message.message import Message

class MessageRepository(AsyncFirestoreCRUD[Message]):
    def __init__(self, company_id: str):
        self.company_id = company_id
        super().__init__(
            collection=f"companies/{company_id}/messages", 
            entitie=Message,            
            )