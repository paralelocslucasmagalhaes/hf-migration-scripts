from fastapi import APIRouter, HTTPException, status
from domain.entities.chat import Chat
from fastapi import Depends
from api.v1.schemas.chat import HandoffRequest
from api.v1.schemas.chat import ChatFilter
from typing import List
from fastapi import Query
from application.use_cases.chat.chat import ChatService
from application.use_cases.chat.message import MessageService
from api.v1.dependencies.legacy.chat import get_handoff_use_case
from api.v1.dependencies.legacy.chat import get_chat_use_case
from api.v1.dependencies.legacy.message import get_chat_message_use_case
from domain.entities.message.message import Message


router = APIRouter()

@router.post("/take_out", response_model=Chat, status_code=status.HTTP_200_OK)
async def take_out_chat(
        payload: HandoffRequest,
        use_case: ChatService = Depends(get_handoff_use_case)
        ):
    try:
        response = await use_case.take_out(chat_id=payload.chat_id, user_id=payload.user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=(e))
    return response

@router.post("/handoff", response_model=Chat, status_code=status.HTTP_200_OK)
async def handoff_chat(
    payload: HandoffRequest,
    use_case: ChatService = Depends(get_handoff_use_case)
    ):
    ## Retrieve Chat Information
    try:
        response = await use_case.human_handoff(chat_id=payload.chat_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=(e))
    return response

@router.post("/closeout", response_model=Chat, status_code=status.HTTP_200_OK)
async def closeout_chat(
        payload: HandoffRequest,
        use_case: ChatService = Depends(get_handoff_use_case)
        ):
    try:
        response = await use_case.closeout(chat_id=payload.chat_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=(e))
    return response

@router.get("/", response_model=List[Chat], status_code=status.HTTP_200_OK)
async def get_chats(
        filters: ChatFilter  = Depends(),
        use_case: ChatService = Depends(get_chat_use_case)
        ):

    filter_payload= filters.model_dump(exclude_none=True)
    limit = filter_payload.pop("limit", 100)
    offset = filter_payload.pop("offset", 0)
    order_by = filter_payload.pop("order_by", "created_date")
    descending = filter_payload.pop("descending", True)

    chats = await use_case.get_all(
            offset=offset, limit=limit, descending=descending, order_by=order_by
    )
    if chats is None:
        raise HTTPException(status_code=404, detail="No chats found")
    return chats


@router.get("/{chat_id}/messages", response_model=List[Message], status_code=status.HTTP_200_OK)
async def get_messages(
    chat_id: str,    
    filters: ChatFilter  = Depends(),
    use_case: MessageService = Depends(get_chat_message_use_case)
):
    
    filter_payload= filters.model_dump(exclude_none=True)
    limit = filter_payload.pop("limit", 100)
    offset = filter_payload.pop("offset", 0)
    order_by = filter_payload.pop("order_by", "created_date")
    descending = filter_payload.pop("descending", True)
    
    wheres = [
        ["chat_id", "==", chat_id]
    ]
        
    return await use_case.get_all(limit=limit, offset=offset,descending=descending, wheres=wheres)