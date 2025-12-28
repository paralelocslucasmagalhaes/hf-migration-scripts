from abc import ABC, abstractmethod

class IPublishMessage(ABC):

    @abstractmethod
    async def publish(self, message: dict) -> None:
        pass