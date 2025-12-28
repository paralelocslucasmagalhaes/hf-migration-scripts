from __future__ import annotations
from domain.interface.infra.db import IRepository

from domain.entities.product.product_category import ProductCategory

class IProductCategoryRepository(IRepository[ProductCategory]):
    pass