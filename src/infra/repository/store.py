from infra.db.base_async import AsyncFirestoreCRUD
from domain.entities.store import Store

class StoreRepository(AsyncFirestoreCRUD[Store]):
    def __init__(self, company_id: str):
        self.company_id = company_id
        super().__init__(
            collection=f"companies/{company_id}/stores", 
            entitie=Store,            
            )