
from abc import ABC, abstractmethod
from domain.entities.apps.app import App

class IAsyncAuth(ABC):

    @abstractmethod
    async def is_authenticated(self, app_id: str) -> App | None:
        pass

    @abstractmethod
    async def is_verified(self, app_id: str, verified_token: str) -> bool:
        pass
