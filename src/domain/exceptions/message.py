from domain.exceptions.domain import DomainNotFoundException
from domain.exceptions.domain import DomainAlredyExistsException


class MessageNotFoundError(DomainNotFoundException):
    def __init__(self, conversation_id: str):
        self.message = f"Mensagem não encontrada para o conversation ID {conversation_id} não foi encontrado."
        super().__init__(self.message)