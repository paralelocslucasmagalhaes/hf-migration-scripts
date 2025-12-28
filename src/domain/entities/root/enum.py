from enum import Enum

class Status(str, Enum):
    active = "active"
    deactive = "inactive"
    pending = "pending"