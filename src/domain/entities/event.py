from dataclasses import dataclass, field
from datetime import datetime

@dataclass(kw_only=True)
class Event:
    platform_message_id: str = field(default=None, metadata={"description": "Platform message id"})
    status:  str = field(default=None, metadata={"description": "Platform message id"})
    created_date: datetime = field(metadata={"description": "Timestamp of the message"})