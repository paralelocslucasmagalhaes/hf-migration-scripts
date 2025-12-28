from domain.entities.whatsapp.template import TemplateLanguageEnum
from domain.entities.whatsapp.template import ComponentType
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from typing import List

class TypeParams(str, Enum):
    """The acceptable media formats for the HEADER component."""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"
    CURRENCY = "currency"
    DATE_TIME = "date_time"

@dataclass(kw_only=True)
class Currency:
    fallback_value: str
    code: str
    amount_1000: int

@dataclass(kw_only=True)
class DateTime:
    fallback_value: str
    day_of_week: Optional[int] = None
    year: Optional[int] = None
    month: Optional[int] = None
    day_of_month: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None
    calendar: str = "GREGORIAN"

@dataclass(kw_only=True)
class TemplateParams:
    type: Optional[TypeParams] = field(default=TypeParams.TEXT, metadata={"description": "Type"})
    image: Optional[str] = field(default=None, metadata={"description": "Image media"})
    text: Optional[str] = field(default=None, metadata={"description": "Text"})
    parameter_name: Optional[str] = field(default=None, metadata={"description": "Text"})
    currency: Optional[Currency] = None
    date_time: Optional[DateTime] = None

    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = TypeParams(self.type)


@dataclass(kw_only=True)
class TemplateHeader:
    parameters: List[TemplateParams]
    def __post_init__(self):
        """Validações de Domínio"""
        
        if isinstance(self.parameters, list):
            self.parameters = [TemplateParams(** item) for item in self.parameters]

@dataclass(kw_only=True)
class TemplateBody:
    parameters: List[TemplateParams]
    def __post_init__(self):
        """Validações de Domínio"""
        
        if isinstance(self.parameters, list):
            self.parameters = [TemplateParams(** item) for item in self.parameters]

@dataclass(kw_only=True)
class TemplateButtons:
    parameters: List[TemplateParams]
    sub_type: Optional[str] = None
    index: Optional[str] = None

    def __post_init__(self):
        """Validações de Domínio"""

        if isinstance(self.parameters, list):
            self.parameters = [TemplateParams(** item) for item in self.parameters]


@dataclass(kw_only=True)
class Template:
    name: str
    language: TemplateLanguageEnum
    headers: Optional[TemplateHeader] = field(default=None, metadata={"description": "Media id"})
    body: Optional[TemplateBody] = field(default=None, metadata={"description": "Media id"})
    buttons: Optional[TemplateButtons] = field(default=None, metadata={"description": "Media id"})

    def __post_init__(self):
        """Validações de Domínio"""
        if isinstance(self.language, str):
            self.language = TemplateLanguageEnum(self.language)

        if isinstance(self.headers, dict):
            self.headers = TemplateHeader(** self.headers)
        if isinstance(self.body, dict):
            self.body = TemplateBody(** self.body)
        if isinstance(self.buttons, dict):
            self.buttons = TemplateButtons(** self.buttons)
