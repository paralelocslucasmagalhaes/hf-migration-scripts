
from pydantic import BaseModel
from datetime import datetime


from enum import Enum

class CollectionEnum(str, Enum):
    companies = "companies"
    stores = "stores" 
    agents = "agents"
    products = "products"
    product_categories = "product_categories"
    consumers = "consumers"
    chats = "chats"
    messages = "messages"
    users = "users"
    apps = "apps"
    memberships = "memberships"
    all = "all"


class MigrateRequest(BaseModel):
    company_id: str  # <--- Este campo vai definir qual Repo usar
    collection: CollectionEnum
    created_date: datetime    