from infra.db.base_async import AsyncFirestoreCRUD
from domain.entities.user import User

class UserRepository(AsyncFirestoreCRUD[User]):
    def __init__(self):        
        super().__init__(
            collection=f"users", 
            entitie=User,            
            )