from __future__ import annotations # <--- Adicione isso no topo do arquivo!
from infra.db.base_async_no_model import AsyncFirestoreCRUD
from typing import TypeVar

T = TypeVar('T')

class IntegrationRepository(AsyncFirestoreCRUD[T]):
    def __init__(self):        
        super().__init__(
            collection=f"integrations", 
            entitie=T,            
            )