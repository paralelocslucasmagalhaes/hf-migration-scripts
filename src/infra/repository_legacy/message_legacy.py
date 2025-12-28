from infra.db.base_async_no_model import AsyncFirestoreCRUD
from domain.entities.message.message import Message

class MessageRepository(AsyncFirestoreCRUD[Message]):
    def __init__(self, company_id: str, chat_id:str):
        self.company_id = company_id
        self.chat_id = chat_id
        super().__init__(
            collection=f"companies/{company_id}/chats/{chat_id}/messages", 
            entitie=Message,            
            )