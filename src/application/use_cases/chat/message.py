from domain.interface.repository.message import IMessageRepository
from domain.exceptions.domain import DomainException
from domain.entities.message.message import Message
from domain.entities.event import Event
from typing import List
from dataclasses import asdict
import asyncio 
from domain.entities.message.message import MessageOutgoingUpdate
from datetime import datetime

class MessageService:

    def __init__(self,
                 message_repository: IMessageRepository,
                 ):
        self.message_repository = message_repository

    async def add(self, messages: List[Message]) -> List[Message]:
        try:
            return [await self.message_repository.add(message) for message in messages]
        except DomainException as e:
            raise DomainException(e)
        
    async def get_by_column(self, column: str, operator: str, value: str) -> List[Message] | None:
        try:
            return await self.message_repository.get_list_by(field=column,condition=operator,value=value)
        except DomainException as e:
            raise DomainException(e)
        
    async def get_all(self, limit: int = 100, offset: int = 0, order_by: str = "created_date", descending: bool = True, wheres: list = []) -> List[Message] | None:
        try:
            return await self.message_repository.get_all(limit=limit,offset=offset,order_by=order_by ,descending=descending,wheres=wheres)
        except DomainException as e:
            raise DomainException(e)

    async def _update_events_status(self, event: Event) -> List[Message]:
        messages = []
        message_data = await self.message_repository.get_list_by(field="platform_message_id", condition="==", value=event.platform_message_id)
        if len(message_data) < 1:
            return []
        for message in message_data:
            message.update_status(event.status, event.created_date)
            updated = await self.message_repository.update(message.id, document=asdict(message))
            messages.append(updated)
        return messages
    
    
    async def update_events(self, events: List[Event]) -> List[Message]:
        try:

            return [await self._update_events_status(event=event) for event in events]
        except DomainException as e:
            raise DomainException(e)
    
    async def _update_outgoing_response(self, outgoing_message: MessageOutgoingUpdate) -> Message:
        message = await self.message_repository.get(id=outgoing_message.id)
        message.update_status(status=outgoing_message.status)
        message.update_platform_message_id(platform_message_id=outgoing_message.platform_message_id)
        return await self.message_repository.update(message.id, document=asdict(message))


    async def update_outgoing_response(self, messages: List[MessageOutgoingUpdate]) -> List[dict]:
        try:
            return [await self._update_outgoing_response(outgoing_message=message) for message in messages]
        except DomainException as e:
            raise DomainException(e)        