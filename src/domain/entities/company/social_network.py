from domain.entities.company.enum import SocialNetworksEnum
from dataclasses import dataclass, field

@dataclass(kw_only=True)
class CompanySocialNetworks:
    profile: str 
    social_network: SocialNetworksEnum