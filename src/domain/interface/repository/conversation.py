from __future__ import annotations
from domain.interface.infra.db import IRepository
from domain.entities.conversation import Conversation
class IConversationRepository(IRepository[Conversation]):
    pass