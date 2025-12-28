from infra.db.base_async_no_model import AsyncFirestoreCRUD
from domain.entities.company import Company

class CompanyRepository(AsyncFirestoreCRUD[Company]):
    def __init__(self):        
        super().__init__(
            collection=f"companies", 
            entitie=Company,            
            )