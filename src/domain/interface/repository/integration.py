from __future__ import annotations
from domain.interface.infra.db import IRepository
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List

T = TypeVar('T')

class IIntegrationRepository(IRepository[T]):
    pass