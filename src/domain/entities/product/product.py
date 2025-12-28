from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from domain.entities.product.enum import ProductStatus
from domain.entities.product.enum import PricePrefix
from domain.entities.product.enum import CurrencyCoin
from domain.entities.product.enum import CurrencySymbol

@dataclass(kw_only=True)
class Currency:
    coin: CurrencyCoin = field(default=CurrencyCoin.BRL, metadata={"description":"Currency coin, e.g. USD"})
    symbol: CurrencySymbol = field(default=CurrencySymbol.BRL, metadata={"description":"Currency symbol, e.g. $"})

    def __post_init__(self):
        """
        Lógica de inicialização para converter tipos brutos (strings/dicts) 
        em objetos de domínio.
        """
        # 1. Tratamento de Enums (converte string para Enum se necessário)
        if isinstance(self.coin, str):
            self.coin = CurrencyCoin(self.coin)

        if isinstance(self.symbol, str):
            self.symbol = CurrencySymbol(self.symbol)

@dataclass(kw_only=True)
class Product:
    id: str
    name: str
    status: ProductStatus
    created_date: datetime
    updated_date: datetime
    company_id: str
    price: float

    # Campos opcionais ou com default sempre ao final
    description: Optional[str] = None
    photo_url: Optional[str] = None
    currency: Optional[Currency] = None
    price_prefix: Optional[PricePrefix] = PricePrefix.exactly
    category_id: Optional[str] = None
    

    def __post_init__(self):
        """
        Lógica de inicialização para converter tipos brutos (strings/dicts) 
        em objetos de domínio.
        """
        # 1. Tratamento de Enums (converte string para Enum se necessário)
        if isinstance(self.status, str):
            self.status = ProductStatus(self.status)
        
        if isinstance(self.price_prefix, str):
            self.price_prefix = PricePrefix(self.price_prefix)

        # 2. Tratamento de Datas (converte string ISO para datetime)
        if isinstance(self.created_date, str):
            self.created_date = datetime.fromisoformat(self.created_date)
        
        if isinstance(self.updated_date, str):
            self.updated_date = datetime.fromisoformat(self.updated_date)
            
        if isinstance(self.currency, dict):
            self.currency = Currency(**self.currency)