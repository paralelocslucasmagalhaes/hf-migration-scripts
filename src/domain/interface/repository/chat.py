from __future__ import annotations
from domain.interface.infra.db import IRepository

from domain.entities.chat import Chat

class IChatRepository(IRepository[Chat]):
    pass