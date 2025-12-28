from domain.interface.repository.conversation import IConversationRepository
from domain.exceptions.domain import DomainException
from domain.entities.conversation import Conversation

class ConversationService:

    def __init__(self,
                 conversation_repository: IConversationRepository
                 ):
        self.conversation_repository = conversation_repository

    async def add(self, conversation: Conversation) -> Conversation:

        wheres = [
            ["contact.platform_id", "==", conversation.contact.platform_id],
            ["end_conversation", "==", False]
        ]
        try:
            data = await self.conversation_repository.get_all(wheres=wheres)
            if len(data) > 0:
                return data[0]
            return await self.conversation_repository.add(document=conversation)
        except DomainException as e:
            raise DomainException(e)       