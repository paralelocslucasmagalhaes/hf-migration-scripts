from infra.db.base_async import AsyncFirestoreCRUD
from domain.entities.root.params import Params

class ParamsRepository(AsyncFirestoreCRUD[Params]):
    def __init__(self):        
        super().__init__(
            collection=f"params", 
            entitie=Params,            
            )