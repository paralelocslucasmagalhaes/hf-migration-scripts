from infra.repository.store import StoreRepository
from pydantic import BaseModel
from fastapi import Depends

def get_store_respository(company_id: str) ->StoreRepository:
    return StoreRepository(company_id=company_id)