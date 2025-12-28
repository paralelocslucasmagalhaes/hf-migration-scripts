from domain.interface.infra.http_async_client import IHttpAsyncClient
from domain.interface.auth import IAsyncAuth

import os
from domain.entities.apps.app import App


class AuthAccountAdapter(IAsyncAuth):
    
    def __init__(self, 
                 http_async_client: IHttpAsyncClient):
        self.base_url = os.getenv("URL_ACCOUNT_SERVICE", "https://auth-account-service.fly.dev")
        self.integration_path = "apps"
        self.api_version = "api/v1"
        self.http_async_client = http_async_client

    async def is_authenticated(self, app_id: str) -> dict | None:
        url = f"{self.base_url}/{self.api_version}/{self.integration_path}/{app_id}"
        response = await self.http_async_client.get(url)
        if response is None:
            return None
        return response
    
    async def is_verified(self, app_id: str) -> bool:
        url = f"{self.base_url}/{self.api_version}/{self.integration_path}/{app_id}"
        response = await self.http_async_client.get(url)
        if response is None:
            return False
        return True