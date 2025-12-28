from abc import ABC, abstractmethod
from typing import List
from typing import Any, Optional


class ITasksClient(ABC):

    @abstractmethod
    async def add(self, url: str, audience: str, payload: dict, delay_seconds: int, service_account: str, task_name: Optional[str] = None, queue: Optional[str] = None) -> str:
        pass

    @abstractmethod
    async def put(self, task_id: str,url: str, audience: str, payload: dict, delay_seconds: int, service_account: str, queue: Optional[str] = None) -> str:
        pass
    
    @abstractmethod
    async def delete(self, task_id: str) -> str:
        pass


class ITaskService(ABC):

    @abstractmethod
    async def add(self, payload: dict, delay_seconds: int) -> str:
        pass

    @abstractmethod
    async def put(self, task_id: str,payload: dict, delay_seconds: int) -> str:
        pass
    
    @abstractmethod
    async def delete(self, task_id: str) -> str:
        pass


