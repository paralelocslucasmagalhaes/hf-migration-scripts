from __future__ import annotations
from domain.interface.infra.db import IRepository
from domain.entities.user import User
class IUserRepository(IRepository[User]):
    pass