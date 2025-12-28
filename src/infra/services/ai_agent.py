from domain.interface.infra.http_async_client import IHttpAsyncClient


import os
from domain.entities.apps.app import App


class AiAsyncAgentAdapter():
    
    def __init__(self, 
                 http_async_client: IHttpAsyncClient):
        self.base_url = os.getenv("URL_AGENT_SERVICE", "https://auth-account-service.fly.dev")
        self.api_version = "api/v1"
        self.path = "webhook"
        self.http_async_client = http_async_client

    async def post(self, message: dict) -> dict | None:
        url = f"{self.base_url}/{self.api_version}/{self.path}"
        response = await self.http_async_client.post(url, payload=message)
        if response is None:
            return None
        return response