from dataclasses import dataclass, field
from typing import Optional
from domain.entities.platform import PlatformEnum
from domain.entities.whatsapp.outgoing import WhatsAppOutgoingResponse


@dataclass(kw_only=True)
class OutgoingMessageResponse():
    company_id: Optional[str] = field(default=None, metadata={"description": "Company id"})
    app_id: Optional[str] = field(default=None, metadata={"description": "App id"})
    message_id: Optional[str] = field(default=None, metadata={"description": "Message id"})
    platform: PlatformEnum = field(metadata={"description": "Platform Message channel"})
    whatsapp: Optional[WhatsAppOutgoingResponse] = field(default=None, metadata={"description": "Whatsapp outgoing"})
    def __post_init__(self):
        """Validações de Domínio"""

        if isinstance(self.platform, str):
            self.platform = PlatformEnum(self.platform)

        if isinstance(self.whatsapp, dict):
            self.whatsapp = WhatsAppOutgoingResponse(** self.whatsapp)