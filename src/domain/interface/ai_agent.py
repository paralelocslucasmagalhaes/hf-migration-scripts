from abc import ABC, abstractmethod
from typing import List


class IAgentAsyncClient(ABC):

    @abstractmethod
    async def post(self, message: dict) -> dict:
        pass


