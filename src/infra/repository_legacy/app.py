from infra.db.base_async_no_model import AsyncFirestoreCRUD
from domain.entities.apps.app import App

class AppRepository(AsyncFirestoreCRUD[App]):
    def __init__(self):        
        super().__init__(
            collection=f"apps", 
            entitie=App,            
            )