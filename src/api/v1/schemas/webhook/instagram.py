from pydantic import Field
from typing import List, Optional, Literal
from pydantic import BaseModel

class IntagramWebhook(BaseModel):
    entry: List[dict]
    object: str