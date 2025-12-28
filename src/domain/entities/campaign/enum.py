from enum import Enum

class StatusCampaignEnum(str, Enum):    
    draft = "draft"
    pending = "pending"
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"

class StatusContactCampaignEnum(str, Enum):    
    active = "active"
    deactive = "inactive"