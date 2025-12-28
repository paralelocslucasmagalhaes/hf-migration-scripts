from abc import ABC, abstractmethod
from typing import List


class PubSubAsyncClient(ABC):

    @abstractmethod
    async def publish(self, topic: str, message: dict) -> str:
        pass

    @abstractmethod
    async def subscribe(self, topic: str, callback) -> bool:
        pass

    @abstractmethod
    async def unsubscribe(self, topic: str, callback) -> bool:
        pass