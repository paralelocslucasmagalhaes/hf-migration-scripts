from __future__ import annotations
from domain.interface.infra.db import IRepository
from domain.entities.product.product import Product

class IProductRepository(IRepository[Product]):
    pass