from infra.db.base_async import AsyncFirestoreCRUD
from domain.entities.company import Company

class CompanyRepository(AsyncFirestoreCRUD[Company]):
    def __init__(self):        
        super().__init__(
            collection=f"companies", 
            entitie=Company,            
            )