from infra.db.base_async_no_model import AsyncFirestoreCRUD
from domain.entities.user import User

class UserRepository(AsyncFirestoreCRUD[User]):
    def __init__(self):        
        super().__init__(
            collection=f"users", 
            entitie=User,            
            )