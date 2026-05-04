"""
routers/image.py
-----------------
GET  /api/background-image   → generate image (query params)
POST /api/background-image   → generate image (full body, saves to history)

The POST variant requires auth and a session_id so the generated image
is persisted to MongoDB alongside chat messages.
The GET variant is kept auth-optional for the canvas background fetch
(which doesn't need to be saved to history).
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query

from core.dependencies import get_optional_user
from models.image import ImageRequest, ImageResponse
from services.image_service import generate_image
from services.message_service import save_image_message

router = APIRouter(prefix="/api", tags=["image"])


@router.get(
    "/background-image",
    response_model=ImageResponse,
    summary="Generate a floor plan image (canvas background, not saved to history)",
)
def background_image_get(
        prompt: Optional[str] = Query(default=None),
        width: Optional[int] = Query(default=None, ge=64, le=1024),
        height: Optional[int] = Query(default=None, ge=64, le=1024),
        steps: Optional[int] = Query(default=None, ge=1, le=150),
        seed: Optional[int] = Query(default=None),
) -> ImageResponse:
    result = generate_image(
        prompt=prompt or "floor plan architectural drawing",
        width=width,
        height=height,
        steps=steps,
        seed=seed,
    )
    return ImageResponse(**result)


@router.post(
    "/background-image",
    response_model=ImageResponse,
    summary="Generate an image from chat (/image command) — saved to message history",
)
async def background_image_post(
        body: ImageRequest,
        current_user: Optional[dict] = Depends(get_optional_user),
) -> ImageResponse:
    result = generate_image(
        prompt=body.prompt,
        width=body.width,
        height=body.height,
        steps=body.steps,
        guidance_scale=body.guidance_scale,
        lora_scale=body.lora_scale,
        seed=body.seed,
    )

    # Persist to MongoDB when called from the chat panel (auth + session_id present)
    if current_user and body.session_id:
        user_id = current_user["sub"]

        # Save the user's /image prompt as a user message
        await save_image_message(
            user_id=user_id,
            session_id=body.session_id,
            role="user",
            prompt=body.prompt,
            dataUrl="",  # user side: no image yet
            model="",
        )

        # Save the generated image as an assistant message
        await save_image_message(
            user_id=user_id,
            session_id=body.session_id,
            role="assistant",
            prompt=body.prompt,
            dataUrl=result["dataUrl"],
            model=result["model"],
        )

    return ImageResponse(**result)
