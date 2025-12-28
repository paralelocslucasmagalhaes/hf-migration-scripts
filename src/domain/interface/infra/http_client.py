from abc import ABC, abstractmethod
from typing import List

class IHttpClient(ABC):

    @abstractmethod
    def get(self, url: str, headers: dict = {}, params: dict = {}) -> dict:
        pass

    @abstractmethod
    def post(self, url: str, payload: dict, headers: dict = {}, params: dict = {} ) -> dict:
        pass

    @abstractmethod
    def put(self, url: str, payload: dict, headers: dict = {}) -> dict:
        pass
    
    @abstractmethod
    def delete(self, url: str, headers: dict = {}) -> dict:
        pass    


