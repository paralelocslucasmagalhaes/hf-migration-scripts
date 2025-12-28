from dataclasses import dataclass, field

from typing import Optional
from typing import List


@dataclass(kw_only=True)
class WhatsAppContactResponse:
    input: Optional[str] = None
    wa_id: Optional[str] = None

@dataclass(kw_only=True)
class WhatsAppMessageResponse:
    id: Optional[str] = None
    message_status: Optional[str] = None
    

@dataclass(kw_only=True)  
class WhatsAppOutgoingResponse:
    messaging_product: Optional[str] = None
    contacts: Optional[List[WhatsAppContactResponse]] = None
    messages: Optional[List[WhatsAppMessageResponse]] = None

    def __post_init__(self):
        """Validações de Domínio"""

        if isinstance(self.contacts, list):
            self.contacts = [WhatsAppContactResponse(** contact) for contact in self.contacts]

        if isinstance(self.messages, list):
            self.messages = [WhatsAppMessageResponse(** item) for item in self.messages]
        