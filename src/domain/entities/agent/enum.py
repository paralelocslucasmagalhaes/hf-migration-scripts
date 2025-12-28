
from enum import Enum

class AgentStatus(str, Enum):
    active = "active"
    inactive = "inactive" # Corrigido de 'deactive' para 'inactive' conforme o valor