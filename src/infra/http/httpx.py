import json
import logging
import httpx
from httpx import BasicAuth
from domain.interface.infra.http_async_client import IHttpAsyncClient
from google.auth.transport.requests import Request
from google.oauth2 import id_token


class HttpXClient(IHttpAsyncClient):

    def __init__(self) -> None:
        pass

    def _get_token(self, url: str):
        return id_token.fetch_id_token(Request(), url)

    async def post(self, url: str, payload: dict, headers: dict = {}, auth: httpx.BasicAuth = None):

        id_token_val = self._get_token(url)
        headers["Content-Type"]= "application/json"
        headers["Authorization"]= f"Bearer {id_token_val}"

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(url, headers=headers, data=json.dumps(payload, default=str), auth=auth)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logging.error(e)
            raise

    async def get(self, url: str, headers: dict = {}, params: dict = {}):
        
        id_token_val = self._get_token(url)
        headers["Content-Type"]= "application/json"
        headers["Authorization"]= f"Bearer {id_token_val}"

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.get(url, params=params, headers=headers)
                if response.status_code >= 300:
                    return None
                return response.json()
        except Exception as e:
            logging.error(e)
            return None   
        
    async def put(self, url: str, payload: dict, headers: dict = {}) -> dict:
        pass
    
    async def delete(self, url: str, headers: dict = {}) -> dict:
        pass    