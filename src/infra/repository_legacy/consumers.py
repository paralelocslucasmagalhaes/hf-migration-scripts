from infra.db.base_async_no_model import AsyncFirestoreCRUD
from domain.entities.contact import Contact

class ConsumerstRepository(AsyncFirestoreCRUD[Contact]):
    def __init__(self, company_id):
        self.company_id = company_id       

        super().__init__(
            collection=f"companies/{company_id}/consumers", 
            entitie=Contact,            
            )