from infra.db.base_async import AsyncFirestoreCRUD
from domain.entities.membership import Membership

class MembershipRepository(AsyncFirestoreCRUD[Membership]):
    def __init__(self):        
        super().__init__(
            collection=f"memberships", 
            entitie=Membership,            
            )