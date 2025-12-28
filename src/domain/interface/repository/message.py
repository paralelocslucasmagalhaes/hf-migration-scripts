from __future__ import annotations
from domain.interface.infra.db import IRepository

from domain.entities.message.message import Message

class IMessageRepository(IRepository[Message]):
    pass