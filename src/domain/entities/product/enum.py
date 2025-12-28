from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

class ProductStatus(str, Enum):
    active = "active"
    inactive = "inactive"    

class PricePrefix(str, Enum):
    exactly = "exactly"
    _from = "from"

class CurrencyCoin(str, Enum):
    USD = "USD"
    BRL = "BRL"

class CurrencySymbol(str, Enum):
    USD = "$"
    BRL = "R$"
