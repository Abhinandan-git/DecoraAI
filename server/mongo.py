"""
mongo.py
--------
MongoDB Atlas connection via Motor (async driver).

All MongoDB concerns live here — services import collection accessors,
never the raw client, keeping them easy to test and swap.

Collections
-----------
  messages   — every chat text message and generated image, one doc per turn
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo import ASCENDING, DESCENDING

from core.config import get_settings

if TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)
settings = get_settings()

# ── Singleton client ──────────────────────────────────────────────────────────

_client: AsyncIOMotorClient | None = None
_db: "AsyncIOMotorDatabase | None" = None


async def connect() -> None:
    """Open the Motor connection pool and ensure indexes exist."""
    global _client, _db

    _client = AsyncIOMotorClient(
        settings.mongodb_uri,
        serverSelectionTimeoutMS=5_000,
    )
    _db = _client[settings.mongodb_db_name]

    await _ensure_indexes()
    logger.info("MongoDB connected — db: %s", settings.mongodb_db_name)


async def disconnect() -> None:
    """Close the Motor connection pool gracefully."""
    global _client, _db
    if _client is not None:
        _client.close()
        _client = None
        _db = None
        logger.info("MongoDB disconnected.")


def _get_db() -> "AsyncIOMotorDatabase":
    if _db is None:
        raise RuntimeError("MongoDB not connected. Was connect() called in lifespan?")
    return _db


# ── Collection accessors ──────────────────────────────────────────────────────

def messages_col() -> AsyncIOMotorCollection:
    """
    The messages collection.

    Schema (one document per message turn):
    {
        _id:         ObjectId  (auto)
        user_id:     str       — who sent / triggered this message
        session_id:  str       — groups messages into a conversation
        role:        str       — "user" | "assistant"
        kind:        str       — "text" | "image"
        content:     str       — text body  (kind="text")
        dataUrl:    str|None  — base64 PNG  (kind="image")
        prompt:      str|None  — generation prompt (kind="image")
        model:       str|None  — "lora" | "fallback"  (kind="image")
        created_at:  datetime
    }
    """
    return _get_db()["messages"]


# ── Index creation ────────────────────────────────────────────────────────────

async def _ensure_indexes() -> None:
    col = messages_col()

    # Primary query pattern: fetch all messages for a session in order
    await col.create_index(
        [("user_id", ASCENDING), ("session_id", ASCENDING), ("created_at", ASCENDING)],
        name="user_session_time",
    )

    # Secondary: list sessions for a user (most recent first)
    await col.create_index(
        [("user_id", ASCENDING), ("created_at", DESCENDING)],
        name="user_time_desc",
    )

    logger.debug("MongoDB indexes ensured.")
