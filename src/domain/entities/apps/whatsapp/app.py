from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from datetime import datetime

# Assumi uma definição simples para o Enum Status
class Status(str, Enum):
    active = "active"
    deactive = "deactive"

@dataclass(kw_only=True)
class WhatsAppApp:
    # --- Campos Obrigatórios (Sem default) ---
    app_id: str = field(metadata={"description": "Whatsapp App ID"})
    name: str = field(metadata={"description": "Whatsapp App Name"})
    waba_id: str = field(metadata={"description": "Whatsapp Business Account ID"})
    
    pin: Optional[str] = field(default=None, metadata={"description": "Whatsapp Pin"})
    
    # --- Campos com Default ---
    meta_status: Optional[Status] = field(
        default=Status.deactive, 
        metadata={"description": "Meta App Status"}
    )
    register_phone_status: Optional[Status] = field(
        default=Status.deactive, 
        metadata={"description": "WhatsApp Register Phone Status"}
    )
    subscribed_status: Optional[Status] = field(
        default=Status.deactive, 
        metadata={"description": "Whether the app is subscribed to webhooks"}
    )
    
    # --- Campos Opcionais (Nullable) ---
    verified_name: Optional[str] = field(
        default=None, 
        metadata={"description": "Verified Name"}
    )
    quality_rating: Optional[str] = field(
        default=None, 
        metadata={"description": "Quality rating"}
    )
    phone_number: Optional[str] = field(
        default=None, 
        metadata={"description": "Whatsapp Phone Number"}
    )
    phone_number_id: Optional[str] = field(
        default=None, 
        metadata={"description": "Whatsapp Phone Number ID"}
    )
    verified_token: Optional[str] = field(default=None, metadata={"description": "Verified Token for WhatsApp Webhook"})

    token: Optional[str] = field(default=None, metadata={"description": "Whatsapp Pin"})

    def __post_init__(self):
        """Validações de Domínio"""

        if isinstance(self.meta_status, str):
            self.meta_status = Status(self.meta_status)

        if isinstance(self.register_phone_status, str):
            self.register_phone_status = Status(self.register_phone_status)

        if isinstance(self.subscribed_status, str):
            self.subscribed_status = Status(self.subscribed_status)

        if isinstance(self.subscribed_status, str):
            self.subscribed_status = Status(self.subscribed_status)