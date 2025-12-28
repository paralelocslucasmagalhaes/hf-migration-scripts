from __future__ import annotations
from domain.interface.infra.db import IRepository
from domain.entities.membership import Membership

class IMembershipRepository(IRepository[Membership]):
    pass