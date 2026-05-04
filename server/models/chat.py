"""models/chat.py — Chat request / response schemas and stored message shapes."""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


# ── API schemas ───────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4096)
    session_id: str = Field(..., description="Client-generated UUID that groups messages")


class ChatResponse(BaseModel):
    reply: str
    session_id: str


# ── Stored message document ───────────────────────────────────────────────────

MessageRole = Literal["user", "assistant"]
MessageKind = Literal["text", "image"]


class MessageDoc(BaseModel):
    """
    Represents one stored message turn (either direction, either kind).
    Maps 1-to-1 with a MongoDB document in the `messages` collection.
    """
    user_id: str
    session_id: str
    role: MessageRole
    kind: MessageKind

    # text messages
    content: Optional[str] = None

    # image messages
    dataUrl: Optional[str] = None  # base64 PNG — potentially large
    prompt: Optional[str] = None
    model: Optional[str] = None  # "lora" | "fallback"

    created_at: datetime = Field(default_factory=datetime.utcnow)


# ── History / session list responses ─────────────────────────────────────────

class MessageOut(BaseModel):
    """Public-facing message shape returned by the history endpoints."""
    id: str  # MongoDB _id as hex string
    role: MessageRole
    kind: MessageKind
    content: Optional[str]
    dataUrl: Optional[str]
    prompt: Optional[str]
    model: Optional[str]
    created_at: datetime


class SessionOut(BaseModel):
    """Summary of a conversation session."""
    session_id: str
    message_count: int
    last_message: datetime
