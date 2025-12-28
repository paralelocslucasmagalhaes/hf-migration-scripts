from pydantic import Field
from typing import List, Optional, Literal
from pydantic import BaseModel


class Metadata(BaseModel):
    display_phone_number: str
    phone_number_id: str


class Profile(BaseModel):
    name: str

class Contact(BaseModel):
    profile: Profile
    wa_id: str

class WhatsAppText(BaseModel):
    body: str

class WhatsAppMedia(BaseModel):
    id: str
    mime_type: Optional[str] = None
    sha256: Optional[str] = None
    caption: Optional[str] = None  # Para imagens/documentos
    filename: Optional[str] = None # Para documentos
    url: Optional[str] = None   # Para áudio

class WhatsAppLocation(BaseModel):
    latitude: float
    longitude: float
    name: Optional[str] = None
    address: Optional[str] = None

class WhatsAppInteractive(BaseModel):
    type: str
    button_reply: Optional[dict] = None
    list_reply: Optional[dict] = None

class Message(BaseModel):
    from_: str = Field(..., alias="from_", description="Sender user ID or username") # 'from' is a reserved keyword in Python
    id: str
    timestamp: str
    type: Literal["text", "image", "audio", "voice", "document", "sticker", "video", "interactive", "location", "contacts", "unknown"]
    text: Optional[WhatsAppText] = None
    image: Optional[WhatsAppMedia] = None
    audio: Optional[WhatsAppMedia] = None
    voice: Optional[WhatsAppMedia] = None
    document: Optional[WhatsAppMedia] = None
    video: Optional[WhatsAppMedia] = None
    sticker: Optional[WhatsAppMedia] = None
    location: Optional[WhatsAppLocation] = None
    interactive: Optional[WhatsAppInteractive] = None

class Origin(BaseModel):
    type: str

class Conversation(BaseModel):
    id: str
    expiration_timestamp: Optional[str] = None
    origin: Origin

class Pricing(BaseModel):
    billable: bool
    pricing_model: str
    category: str
    type: str

class Statuses(BaseModel):
    id: str
    status: str
    timestamp: str
    recipient_id: str
    conversation: Optional[Conversation] = None
    pricing: Optional[Pricing] = None
    errors: Optional[List[dict]] = None

class Value(BaseModel):
    messaging_product: str
    metadata: Metadata
    contacts: Optional[List[Contact]] = None
    messages: Optional[List[Message]] = None
    statuses: Optional[List[Statuses]] = None


class Change(BaseModel):
    field: str
    value: Value
   
class Entry(BaseModel):
    id: str
    changes: List[Change]

class WhatsAppWebhook(BaseModel):
    entry: List[Entry]
    object: str

class WhatsAppMessage(BaseModel):
    messaging_product: str = "whatsapp"
    recipient_type: str = "individual"
    to: str
    type: str = "text"    
    text: WhatsAppText