from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class ButtonType(str, Enum):
    """The type of action a button performs."""
    QUICK_REPLY = "QUICK_REPLY"
    PHONE_NUMBER = "PHONE_NUMBER"
    URL = "URL"
    COPY_CODE = "COPY_CODE"
    OTP = "ONE_TIME_PASSWORD"


class URLButtonSubType(str, Enum):
    """The type of URL button used."""
    STATIC = "static"
    DYNAMIC = "dynamic"


class ComponentType(str, Enum):
    """The main structural components of a template message."""
    HEADER = "HEADER"
    BODY = "BODY"
    FOOTER = "FOOTER"
    BUTTONS = "BUTTONS"


class HeaderFormat(str, Enum):
    """The acceptable media formats for the HEADER component."""
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    DOCUMENT = "DOCUMENT"


class TemplateCategoryEnum(str, Enum):
    """Template category."""
    UTILITY = "UTILITY"
    MARKETING = "MARKETING"
    AUTHENTICATION = "AUTHENTICATION"


class TemplateLanguageEnum(str, Enum):
    """Template language locale."""
    en_us = "en_US"
    pt_br = "pt_BR"
    es_es = "es_ES"
    en    = "en"


@dataclass
class TemplateButton:
    """Represents a button in a WhatsApp template."""
    type: ButtonType
    text: Optional[str] = None
    url: Optional[str] = None
    phone_number: Optional[str] = None
    url_type: Optional[URLButtonSubType] = None

    def __post_init__(self):

        if isinstance(self.type, str):
            self.type = ButtonType(self.type)

        if isinstance(self.url_type, str):
            self.url_type = URLButtonSubType(self.url_type)

@dataclass
class ParamNamed:
    example: Optional[dict] = None
    param_name: Optional[dict] = None

@dataclass
class TemplateComponentExample:
    body_text_named_params: Optional[List[ParamNamed]] = field(default_factory=list)
    header_text_named_params: Optional[List[ParamNamed]] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.body_text_named_params, list):
            self.body_text_named_params = [ParamNamed(** item) for item in self.body_text_named_params]

        if isinstance(self.header_text_named_params, list):
            self.header_text_named_params = [ParamNamed(** item) for item in self.header_text_named_params]

@dataclass
class TemplateComponent:
    """Represents a component (header, body, footer, buttons) in a WhatsApp template."""
    type: ComponentType
    text: Optional[str] = None
    format: Optional[HeaderFormat] = None
    example: Optional[TemplateComponentExample] = None

    def __post_init__(self):
        if isinstance(self.example, dict):
            self.example = TemplateComponentExample(** self.example)

        if isinstance(self.format, str):
            self.format = HeaderFormat(self.format)

        if isinstance(self.type, str):
            self.type = ComponentType(self.type)
    


@dataclass(kw_only=True)
class WhatsAppTemplate:
    id: str = field(metadata={"description": "WhatsApp Template id"})
    buttons: Optional[List[TemplateButton]] = field(default_factory=list)
    category: TemplateCategoryEnum = field(default=None, metadata={"description": "WhatsApp Template name"})
    components: List[TemplateComponent] = field(default_factory=list)
    language: TemplateLanguageEnum = field(default=None, metadata={"description": "WhatsApp Template name"})
    name: Optional[str] = field(default=None, metadata={"description": "WhatsApp Template name"})
    parameter_format: Optional[str] = field(default=None, metadata={"description": "WhatsApp parameter_format"})
    status: Optional[str] = field(default=None, metadata={"description": "WhatsApp Template status"})
    sub_category: Optional[str] = None

    def __post_init__(self):

        if isinstance(self.category, str):
            self.category = TemplateCategoryEnum(self.category)

        if isinstance(self.language, str):
            self.language = TemplateLanguageEnum(self.language)

        if isinstance(self.components, list):
            self.components = [TemplateComponent(** item) for item in self.components]

        if isinstance(self.buttons, list):
            self.buttons = [TemplateButton(** item) for item in self.buttons]