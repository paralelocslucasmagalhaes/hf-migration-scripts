from infra.repository_legacy.product_category import ProductCategoryRepository
from fastapi import Depends

def get_product_category_respository(company_id: str) ->ProductCategoryRepository:
    return ProductCategoryRepository(company_id=company_id)