"""
services/chat_service.py
-------------------------
Stateless chat service.

The frontend sends a single message; the backend is responsible for
maintaining any conversation history, RAG context, or system prompts.

To wire up a real LLM:
  1. Set CHAT_ENABLED=true in .env
  2. Uncomment + fill in the relevant provider block below
  3. Add the provider's package to requirements.txt

The function signature `get_reply(message: str) -> str` is the only
contract the router depends on — internals can change freely.
"""

import logging

from core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def get_reply(message: str) -> str:
    """
    Return an assistant reply for `message`.
    Dispatches to whichever provider is configured.
    """
    if not settings.chat_enabled:
        return _placeholder_reply(message)

    # ── OpenAI ───────────────────────────────────────────────────────────────
    # Uncomment and set OPENAI_API_KEY + OPENAI_MODEL in .env
    #
    # try:
    #     from openai import OpenAI
    #     client = OpenAI(api_key=settings.openai_api_key)
    #     completion = client.chat.completions.create(
    #         model=settings.openai_model,
    #         messages=[
    #             {
    #                 "role": "system",
    #                 "content": (
    #                     "You are a helpful floor plan and interior design assistant. "
    #                     "Answer questions about layouts, dimensions, and room planning. "
    #                     "Be concise and practical."
    #                 ),
    #             },
    #             {"role": "user", "content": message},
    #         ],
    #     )
    #     return completion.choices[0].message.content or ""
    # except Exception as exc:
    #     logger.error("OpenAI error: %s", exc)
    #     return f"⚠ Chat service error: {exc}"

    # ── Anthropic Claude ─────────────────────────────────────────────────────
    # Uncomment and set ANTHROPIC_API_KEY in .env
    #
    # try:
    #     import anthropic
    #     client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    #     message_obj = client.messages.create(
    #         model="claude-3-5-sonnet-20241022",
    #         max_tokens=1024,
    #         system=(
    #             "You are a helpful floor plan and interior design assistant. "
    #             "Answer questions about layouts, dimensions, and room planning."
    #         ),
    #         messages=[{"role": "user", "content": message}],
    #     )
    #     return message_obj.content[0].text
    # except Exception as exc:
    #     logger.error("Anthropic error: %s", exc)
    #     return f"⚠ Chat service error: {exc}"

    return _placeholder_reply(message)


# ── Placeholder ───────────────────────────────────────────────────────────────

def _placeholder_reply(message: str) -> str:
    return (
        f'Received: "{message}"\n\n'
        "Chat is not yet connected to an LLM. "
        "Set CHAT_ENABLED=true and configure a provider in "
        "services/chat_service.py.\n\n"
        "Tip: type /image <description> to generate a reference image "
        "you can drag onto the canvas."
    )
