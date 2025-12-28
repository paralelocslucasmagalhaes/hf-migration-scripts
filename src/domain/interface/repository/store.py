from __future__ import annotations
from domain.interface.infra.db import IRepository
from domain.entities.store import Store
class IStoreRepository(IRepository[Store]):
    pass