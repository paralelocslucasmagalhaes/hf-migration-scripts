from infra.repository.product import ProductRepository
from fastapi import Depends

def get_product_respository(company_id: str) ->ProductRepository:
    return ProductRepository(company_id=company_id)