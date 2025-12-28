from typing import Optional
from api.v1.schemas.base import Filter
# Importações mantidas conforme seu original


class MessageChatFilter(Filter):
    company_id: Optional[str] = None