from enum import Enum

class SocialNetworksEnum(str, Enum):       
    instagram = "instagram"
    tiktok = "tiktok"
    facebook = "facebook"


class CompanyStatusEnum(str, Enum):
    active = "active"
    deactive = "inactive"
