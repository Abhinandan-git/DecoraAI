"""
routers/image.py
-----------------
Image generation endpoint.

GET  /api/background-image?prompt=<text>  →  { dataUrl, prompt, width, height, steps, seed, model }
POST /api/background-image                →  same, accepts full ImageRequest body
"""

from typing import Optional

from fastapi import APIRouter, Query

from models.image import ImageRequest, ImageResponse
from services.image_service import generate_image

router = APIRouter(prefix="/api", tags=["image"])


@router.get(
    "/background-image",
    response_model=ImageResponse,
    summary="Generate a floor plan image via GET (prompt as query param)",
)
def background_image_get(
        prompt: Optional[str] = Query(
            default=None,
            description="Natural-language description of the floor plan to generate",
        ),
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
    summary="Generate a floor plan image via POST (full control over parameters)",
)
def background_image_post(body: ImageRequest) -> ImageResponse:
    result = generate_image(
        prompt=body.prompt,
        width=body.width,
        height=body.height,
        steps=body.steps,
        guidance_scale=body.guidance_scale,
        lora_scale=body.lora_scale,
        seed=body.seed,
    )
    return ImageResponse(**result)
