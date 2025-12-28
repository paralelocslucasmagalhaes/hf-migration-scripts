import requests
import json
from google.auth.transport.requests import Request
from google.oauth2 import id_token
import logging
from domain.interface.infra.http_client import IHttpClient

class RequestsClient(IHttpClient):

    def post(self, url: str, payload: dict, headers: dict = {}, params: dict = {}) -> dict | None:
       
        # id_token_val = self.get_auth(self.base_url)
        headers.update({
            "Content-Type": "application/json",
            })

        try:
            response = requests.post(url=url, headers=headers, data=json.dumps(payload), params=params  )
            if response.status_code >= 300:
                return None
            return response.json()
        except Exception as e:
            logging.error(e)
            return None
        
        
    def get(self, url: str, headers: dict = {}, params:dict = {}) -> dict | None:
       
        # id_token_val = self.get_auth(self.base_url)
        headers.update({
            "Content-Type": "application/json",
            # "Authorization": f"Bearer {id_token_val}"
            })

        try:
            response = requests.get(url=url, params= params, headers=headers)
            if response.status_code >= 300:
                return None
            return response.json()
        except Exception as e:
            logging.error(e)
            return None
        
    def delete(self, url: str, headers: dict = {}, params:dict = {}):
       
        # id_token_val = self.get_auth(self.base_url)
        headers.update({
            "Content-Type": "application/json",
            # "Authorization": f"Bearer {id_token_val}"
            })

        try:
            response = requests.delete(url=url, params= params, headers=headers)
            if response.status_code >= 300:
                return None
            return response.json()
        except Exception as e:
            logging.error(e)
            return None
        
    def put(self, url: str, payload: dict, headers: dict = {}, params: dict = {}) -> dict:
       
        # id_token_val = self.get_auth(self.base_url)
        headers.update({
            "Content-Type": "application/json",
            })

        try:
            response = requests.put(url=url, headers=headers, data=json.dumps(payload), params=params  )
            if response.status_code >= 300:
                return None
            return response.json()
        except Exception as e:
            raise(e)

    def get_auth(self, url: str):
        target_audience = url  # or the Cloud Run service URL
        return id_token.fetch_id_token(Request(), target_audience)

       



