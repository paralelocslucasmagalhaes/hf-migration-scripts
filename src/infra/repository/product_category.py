from infra.db.base_async import AsyncFirestoreCRUD
from domain.entities.product.product_category import ProductCategory

class ProductCategoryRepository(AsyncFirestoreCRUD[ProductCategory]):
    def __init__(self, company_id: str):
        self.company_id = company_id
        super().__init__(
            collection=f"companies/{company_id}/product_categories", 
            entitie=ProductCategory,            
            )