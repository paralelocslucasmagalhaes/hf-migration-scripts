from infra.db.base_async import AsyncFirestoreCRUD
from domain.entities.apps.template import Template

class TemplateRepository(AsyncFirestoreCRUD[Template]):
    def __init__(self, app_id: str):
        self.app_id = app_id
        super().__init__(
            collection=f"apps/{app_id}/templates", 
            entitie=Template,            
            )