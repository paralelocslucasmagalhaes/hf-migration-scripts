from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass(kw_only=True)
class CampaignSchedule:
    schedule_date: datetime
    created_date: datetime
    updated_date: datetime
    task_id: Optional[str] = None