from typing import Optional
from datetime import time
from dataclasses import dataclass

@dataclass(kw_only=True)
class WorkDaySchedule:
    start: Optional[time] = None
    end: Optional[time] = None

@dataclass(kw_only=True)
class WorkSchedule:
    monday: Optional[WorkDaySchedule] = None
    tuesday: Optional[WorkDaySchedule] = None
    wednesday: Optional[WorkDaySchedule] = None
    thursday: Optional[WorkDaySchedule] = None
    friday: Optional[WorkDaySchedule] = None
    saturday: Optional[WorkDaySchedule] = None
    sunday: Optional[WorkDaySchedule] = None