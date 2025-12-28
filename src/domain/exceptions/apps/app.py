from domain.exceptions.domain import DomainNotFoundException
from domain.exceptions.domain import DomainAlredyExistsException


class AppNotFoundError(DomainNotFoundException):
    def __init__(self, app_id: str):
        self.message = f"App com ID {app_id} não foi encontrado."
        super().__init__(self.message)

class AppAlreadyExistsError(DomainAlredyExistsException):
    def __init__(self, app_id: str):
        self.message = f"App com phone number id {app_id} já está em uso."
        super().__init__(self.message)