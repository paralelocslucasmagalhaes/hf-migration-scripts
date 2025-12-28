from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from domain.entities.product.enum import ProductStatus

@dataclass
class ProductCategory:
    id: str
    status: ProductStatus
    created_date: datetime
    updated_date: datetime
    company_id: str
    name: str
    
    # Campos opcionais ou com default sempre ao final
    description: Optional[str] = None

    def __post_init__(self):
        """
        Lógica de inicialização para converter tipos brutos (strings/dicts) 
        em objetos de domínio.
        """
        # 1. Tratamento de Enums (converte string para Enum se necessário)
        if isinstance(self.status, str):
            self.status = ProductStatus(self.status)

        # 2. Tratamento de Datas (converte string ISO para datetime)
        if isinstance(self.created_date, str):
            self.created_date = datetime.fromisoformat(self.created_date)
        
        if isinstance(self.updated_date, str):
            self.updated_date = datetime.fromisoformat(self.updated_date)