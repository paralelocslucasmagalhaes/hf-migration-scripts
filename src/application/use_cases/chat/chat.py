from domain.interface.repository.chat import IChatRepository
from domain.interface.repository.user import IUserRepository
from domain.exceptions.domain import DomainException
from domain.entities.chat import Chat
from typing import List

from dataclasses import asdict
import logging

class ChatService:

    def __init__(self,
                 chat_repository: IChatRepository,
                 user_repository: IUserRepository,
                 ):
        self.chat_repository = chat_repository
        self.user_repository = user_repository

    async def add(self, chat: Chat) -> Chat:        
        try:
            chat_data = await self.chat_repository.get_list_by(field="contact.platform_id", condition="==", value=chat.contact.platform_id)
            if len(chat_data) > 0:
                return chat_data[0] # Método sempre retorna uma lista
            
            return await self.chat_repository.add(document=chat)
        except DomainException as e:
            raise DomainException(e)       
        
    async def take_out(self, chat_id: str, user_id: str) -> Chat:
        chat = await self.chat_repository.get(id=chat_id)
        user = await self.user_repository.get(id=user_id)

        chat.take_out(user=user)
        logging.info(f"Processing take out for {chat_id}")
        return await self.chat_repository.update(id=chat.id, document=asdict(chat))
    
    async def human_handoff(self, chat_id: str) -> Chat:
        chat = await self.chat_repository.get(id=chat_id)
        chat.human_handoff()
        logging.info(f"Processing human handoff for {chat_id}")
        return await self.chat_repository.update(id=chat.id, document=asdict(chat))
    
    async def closeout(self, chat_id: str) -> Chat:        
        # Implement logic to handle take out order
        chat = await self.chat_repository.get(id=chat_id)
        chat.closeout()
        logging.info(f"Processing closeout for {chat_id}")
        return await self.chat_repository.update(id=chat.id, document=asdict(chat))
    
    async def get_all(self, limit: int = 100, offset: int = 0, order_by: str = "created_date", descending: bool = True, wheres: list = []) -> List[Chat]:
        return await self.chat_repository.get_all(limit=limit, offset=offset, order_by=order_by, descending=descending, wheres= wheres)