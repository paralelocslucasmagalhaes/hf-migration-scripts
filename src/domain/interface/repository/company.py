from __future__ import annotations
from domain.interface.infra.db import IRepository

from domain.entities.company import Company

class ICompanyRepository(IRepository[Company]):
    pass