from abc import ABC, abstractmethod

class IHttpAsyncClient(ABC):

    @abstractmethod
    async def get(self, url: str, headers: dict = {}, params: dict = {}) -> dict:
        pass

    @abstractmethod
    async def post(self, url: str, payload: dict, headers: dict = {}, params: dict = {} ) -> dict:
        pass

    @abstractmethod
    async def put(self, url: str, payload: dict, headers: dict = {}) -> dict:
        pass
    
    @abstractmethod
    async def delete(self, url: str, headers: dict = {}) -> dict:
        pass    


