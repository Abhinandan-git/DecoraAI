"""
routers/chat.py
----------------
POST /api/chat                             → send a message, get a reply
GET  /api/chat/sessions                   → list this user's sessions
GET  /api/chat/sessions/{session_id}      → full message history for a session
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from core.dependencies import get_current_user
from models.chat import ChatRequest, ChatResponse, MessageOut, SessionOut
from services.chat_service import get_reply
from services.message_service import (
    get_session_context,
    get_session_history,
    list_sessions,
    save_text_message,
)

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post(
    "",
    response_model=ChatResponse,
    summary="Send a message and receive an assistant reply",
)
async def chat(
        body: ChatRequest,
        current_user: dict = Depends(get_current_user),
) -> ChatResponse:
    user_id = current_user["sub"]
    session_id = body.session_id

    # 1. Load recent history for context
    history = await get_session_context(user_id, session_id, max_messages=20)

    # 2. Persist the user's message
    await save_text_message(
        user_id=user_id,
        session_id=session_id,
        role="user",
        content=body.message,
    )

    # 3. Generate reply (passes history for multi-turn context)
    try:
        reply = await get_reply(body.message, history)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM error: {exc}")

    # 4. Persist assistant reply
    await save_text_message(
        user_id=user_id,
        session_id=session_id,
        role="assistant",
        content=reply,
    )

    return ChatResponse(reply=reply, session_id=session_id)


@router.get(
    "/sessions",
    response_model=list[SessionOut],
    summary="List all conversation sessions for the current user",
)
async def sessions(
        limit: int = Query(default=50, ge=1, le=200),
        current_user: dict = Depends(get_current_user),
) -> list[SessionOut]:
    return await list_sessions(user_id=current_user["sub"], limit=limit)


@router.get(
    "/sessions/{session_id}",
    response_model=list[MessageOut],
    summary="Fetch full message history for a session",
)
async def session_history(
        session_id: str,
        limit: Optional[int] = Query(default=None, ge=1, le=500),
        current_user: dict = Depends(get_current_user),
) -> list[MessageOut]:
    return await get_session_history(
        user_id=current_user["sub"],
        session_id=session_id,
        limit=limit,
    )
