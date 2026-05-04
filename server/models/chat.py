"""models/chat.py — Chat request / response schemas."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4096)


class ChatResponse(BaseModel):
    reply: str
