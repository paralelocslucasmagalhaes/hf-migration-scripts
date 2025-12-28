from __future__ import annotations # <--- Adicione isso no topo do arquivo!
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List

T = TypeVar('T')

class IRepository(ABC, Generic[T]):

    @abstractmethod
    async def get(self, id: str) -> Optional[T]:
        pass
    
    @abstractmethod
    async def get_list_by(self, field: str, condition: str, value: str) -> List[Optional[T]]:
        pass

    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0, order_by: str = "created_date", descending: bool = True, wheres: list = []) -> List[Optional[T]]:
        pass

    @abstractmethod
    async def get_all_documents(self) -> List[Optional[T]]:
        pass

    @abstractmethod
    async def add(self, document: T) -> T:
        pass

    @abstractmethod
    async def update(self, id: str, document: dict) -> Optional[T]:
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> Optional[T]:
        pass    


