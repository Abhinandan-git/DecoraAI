"""
services/message_service.py
----------------------------
All MongoDB persistence logic for chat messages and generated images.

Public API
----------
  save_message(doc)                          → str (inserted _id)
  get_session_history(user_id, session_id)   → list[MessageOut]
  list_sessions(user_id, limit)              → list[SessionOut]
  get_session_context(user_id, session_id, max_messages) → list[dict]
    └─ Returns plain dicts suitable for passing to an LLM as message history.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

from pymongo import ASCENDING

from models.chat import MessageDoc, MessageOut, SessionOut
from mongo import messages_col

logger = logging.getLogger(__name__)


# ── Write ─────────────────────────────────────────────────────────────────────

async def save_message(doc: MessageDoc) -> str:
    """Persist a message and return its MongoDB _id as a hex string."""
    result = await messages_col().insert_one(doc.model_dump())
    return str(result.inserted_id)


async def save_text_message(
        user_id: str,
        session_id: str,
        role: str,
        content: str,
) -> str:
    doc = MessageDoc(
        user_id=user_id,
        session_id=session_id,
        role=role,  # type: ignore[arg-type]
        kind="text",
        content=content,
    )
    return await save_message(doc)


async def save_image_message(
        user_id: str,
        session_id: str,
        role: str,
        prompt: str,
        dataUrl: str,
        model: str,
) -> str:
    doc = MessageDoc(
        user_id=user_id,
        session_id=session_id,
        role=role,  # type: ignore[arg-type]
        kind="image",
        prompt=prompt,
        dataUrl=dataUrl,
        model=model,
    )
    return await save_message(doc)


# ── Read ──────────────────────────────────────────────────────────────────────

async def get_session_history(
        user_id: str,
        session_id: str,
        limit: Optional[int] = None,
) -> list[MessageOut]:
    """
    Return all messages for a session, oldest first.
    Pass limit to cap results (useful for paginated UIs).
    """
    cursor = (
        messages_col()
        .find({"user_id": user_id, "session_id": session_id})
        .sort("created_at", ASCENDING)
    )
    if limit is not None:
        cursor = cursor.limit(limit)

    docs = await cursor.to_list(length=None)
    return [_to_message_out(d) for d in docs]


async def list_sessions(
        user_id: str,
        limit: int = 50,
) -> list[SessionOut]:
    """
    Return a deduplicated list of sessions for a user,
    sorted by most recent activity.
    """
    pipeline = [
        {"$match": {"user_id": user_id}},
        {
            "$group": {
                "_id": "$session_id",
                "message_count": {"$sum": 1},
                "last_message": {"$max": "$created_at"},
            }
        },
        {"$sort": {"last_message": -1}},
        {"$limit": limit},
    ]
    docs = await messages_col().aggregate(pipeline).to_list(length=None)
    return [
        SessionOut(
            session_id=d["_id"],
            message_count=d["message_count"],
            last_message=d["last_message"],
        )
        for d in docs
    ]


async def get_session_context(
        user_id: str,
        session_id: str,
        max_messages: int = 20,
) -> list[dict]:
    """
    Return the most recent messages as plain dicts for LLM context injection.
    Only text messages are included (images aren't fed back to the LLM).

    Format: [{"role": "user"|"assistant", "content": "..."}]
    """
    cursor = (
        messages_col()
        .find(
            {"user_id": user_id, "session_id": session_id, "kind": "text"},
        )
        .sort("created_at", ASCENDING)
        .limit(max_messages)
    )
    docs = await cursor.to_list(length=None)
    return [{"role": d["role"], "content": d["content"]} for d in docs]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _to_message_out(doc: dict) -> MessageOut:
    return MessageOut(
        id=str(doc["_id"]),
        role=doc["role"],
        kind=doc["kind"],
        content=doc.get("content"),
        dataUrl=doc.get("dataUrl"),
        prompt=doc.get("prompt"),
        model=doc.get("model"),
        created_at=doc.get("created_at", datetime.utcnow()),
    )
