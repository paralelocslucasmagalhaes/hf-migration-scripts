from infra.db.base_async import AsyncFirestoreCRUD
from domain.entities.contact import Contact

class ContactRepository(AsyncFirestoreCRUD[Contact]):
    def __init__(self, company_id):
        self.company_id = company_id       

        super().__init__(
            collection=f"companies/{company_id}/contacts", 
            entitie=Contact,            
            )