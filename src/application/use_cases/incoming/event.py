from domain.entities.event import Event
from domain.interface.message import IMessageRepository
from dataclasses import asdict
import asyncio
from typing import List

class IncomingEventService():

    def __init__(self, 
                 message_service: IMessageRepository):
        self.message_service = message_service

    
    async def whatsapp_event(self, events: List[Event]):
        return await self.message_service.update_events(events=events)
