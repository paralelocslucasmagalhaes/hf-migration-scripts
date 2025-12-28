
from abc import ABC, abstractmethod
from domain.entities.message.message import Message
from typing import List
from domain.entities.message.message import MessageOutgoingUpdate
from domain.entities.event import Event


class IMessageRepository(ABC):

    @abstractmethod
    async def add(self, messages: List[Message]) ->  List[dict] | None:
        pass

    @abstractmethod
    async def get_by_column(self, column: str, operator: str, value: str) -> List[dict] | None:
        pass

    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0, order_by: str = "created_date", descending: bool = True, wheres: list = []) -> List[dict] | None:
        pass

    @abstractmethod
    async def update_outgoing_response(self, messages: List[MessageOutgoingUpdate]) -> List[dict]:
        pass
    
    @abstractmethod
    async def update_events(self, events: List[Event]) -> List[dict]:
        pass