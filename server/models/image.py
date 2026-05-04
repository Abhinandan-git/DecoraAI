"""models/image.py — Image generation request / response schemas."""

from typing import Optional

from pydantic import BaseModel, Field


class ImageRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500)
    session_id: Optional[str] = Field(default=None, description="If provided, saves image to message history")
    width: Optional[int] = Field(default=None, ge=64, le=1024)
    height: Optional[int] = Field(default=None, ge=64, le=1024)
    steps: Optional[int] = Field(default=None, ge=1, le=150)
    guidance_scale: Optional[float] = Field(default=None, ge=1.0, le=20.0)
    lora_scale: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    seed: Optional[int] = Field(default=None)


class ImageResponse(BaseModel):
    dataUrl: str  # "data:image/png;base64,..."
    prompt: str
    width: int
    height: int
    steps: int
    seed: int
    model: str  # "lora" | "fallback"
