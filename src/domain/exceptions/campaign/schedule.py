from domain.exceptions.domain import DomainNotFoundException
from domain.exceptions.domain import DomainAlredyExistsException
from domain.exceptions.domain import DomainException



class ScheduleCampaignException(DomainException):
    def __init__(self, msg: str):
        self.message = msg
        super().__init__(self.message)


class ScheduleCampaignValueError(DomainException):
    def __init__(self, msg: str):
        self.message = msg
        super().__init__(self.message)
