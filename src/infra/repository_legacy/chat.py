from infra.db.base_async_no_model import AsyncFirestoreCRUD
from domain.entities.chat import Chat

class ChatRepository(AsyncFirestoreCRUD[Chat]):
    def __init__(self, company_id: str):
        self.company_id = company_id
        super().__init__(
            collection=f"companies/{company_id}/chats", 
            entitie=Chat,            
            )