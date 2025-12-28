from __future__ import annotations
from domain.interface.infra.db import IRepository

from domain.entities.apps.app import App

class IAppRepository(IRepository[App]):
    pass