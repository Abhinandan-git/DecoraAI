"""
routers/chat.py
----------------
Chat endpoint.

POST /api/chat  →  { reply }
"""

from fastapi import APIRouter

from models.chat import ChatRequest, ChatResponse
from services.chat_service import get_reply

router = APIRouter(prefix="/api", tags=["chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Send a message and receive an assistant reply",
)
def chat(body: ChatRequest) -> ChatResponse:
    reply = get_reply(body.message)
    return ChatResponse(reply=reply)
