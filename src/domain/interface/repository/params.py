from __future__ import annotations
from domain.interface.infra.db import IRepository

from domain.entities.root.params import Params

class IParamsRepository(IRepository[Params]):
    pass