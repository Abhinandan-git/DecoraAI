"""
services/chat_service.py
-------------------------
Async chat service with MongoDB-backed history.

Flow for each /api/chat call:
  1. Load recent session history from MongoDB (text messages only)
  2. Call the configured LLM with full context
  3. Persist user message → MongoDB
  4. Persist assistant reply → MongoDB
  5. Return the reply

The router handles (3) and (4) explicitly so every message is saved
even if something later in the pipeline fails.
"""

from __future__ import annotations

import logging

from core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def get_reply(message: str, history: list[dict]) -> str:
    """
    Generate a reply given the current message and prior session history.

    `history` is a list of {"role": ..., "content": ...} dicts produced by
    message_service.get_session_context() — ready to pass straight to any
    OpenAI-compatible or Anthropic API.
    """
    if not settings.chat_enabled:
        return _placeholder_reply(message)

    # ── OpenAI ───────────────────────────────────────────────────────────────
    # 1. pip install openai
    # 2. In .env: CHAT_ENABLED=true, OPENAI_API_KEY=sk-..., OPENAI_MODEL=gpt-4o
    #
    # try:
    #     from openai import AsyncOpenAI
    #     client = AsyncOpenAI(api_key=settings.openai_api_key)
    #     messages = [
    #         {
    #             "role": "system",
    #             "content": (
    #                 "You are a helpful floor plan and interior design assistant. "
    #                 "Answer questions about layouts, dimensions, and room planning. "
    #                 "Be concise and practical."
    #             ),
    #         },
    #         *history,
    #         {"role": "user", "content": message},
    #     ]
    #     completion = await client.chat.completions.create(
    #         model=settings.openai_model,
    #         messages=messages,
    #     )
    #     return completion.choices[0].message.content or ""
    # except Exception as exc:
    #     logger.error("OpenAI error: %s", exc)
    #     return f"⚠ Chat error: {exc}"

    # ── Anthropic Claude ─────────────────────────────────────────────────────
    # 1. pip install anthropic
    # 2. In .env: CHAT_ENABLED=true, ANTHROPIC_API_KEY=sk-ant-...
    #
    # try:
    #     import anthropic
    #     client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    #     response = await client.messages.create(
    #         model="claude-3-5-sonnet-20241022",
    #         max_tokens=1024,
    #         system=(
    #             "You are a helpful floor plan and interior design assistant. "
    #             "Answer questions about layouts, dimensions, and room planning."
    #         ),
    #         messages=[*history, {"role": "user", "content": message}],
    #     )
    #     return response.content[0].text
    # except Exception as exc:
    #     logger.error("Anthropic error: %s", exc)
    #     return f"⚠ Chat error: {exc}"

    return _placeholder_reply(message)


def _placeholder_reply(message: str) -> str:
    return (
        f'Received: "{message}"\n\n'
        "Chat is not yet connected to an LLM. "
        "Set CHAT_ENABLED=true and configure a provider in "
        "services/chat_service.py.\n\n"
        "Tip: type /image <description> to generate a reference image "
        "you can drag onto the canvas."
    )
