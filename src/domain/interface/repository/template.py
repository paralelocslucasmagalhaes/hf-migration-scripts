from __future__ import annotations
from domain.interface.infra.db import IRepository

from domain.entities.apps.template import Template

class ITemplateRepository(IRepository[Template]):
    pass