from fastapi import Depends
from pydantic import BaseModel
from domain.service.template_message import TemplateMessageGenerator
from infra.repository_legacy.template import TemplateRepository

def get_template_message_generator() -> TemplateMessageGenerator:
    return TemplateMessageGenerator()

def get_template_respository(app_id: str) ->TemplateRepository:
    return TemplateRepository(app_id=app_id)