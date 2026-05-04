"""
core/config.py
--------------
Central configuration loaded from environment variables.
Copy .env.example → .env and fill in your values.
"""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ──────────────────────────────────────────────────────────────────
    app_name: str = "DecoraAI API"
    app_version: str = "1.0.0"
    debug: bool = False

    # ── Database ──────────────────────────────────────────────────────────────
    # Render gives you this under "External Database URL" on your Postgres dashboard.
    # Change postgresql:// → postgresql+asyncpg:// before pasting.
    database_url: str = "postgresql+asyncpg://user:password@localhost/decoraai"

    # ── Database ─────────────────────────────────────────────────────────────
    # Render external URL — change scheme to postgresql+asyncpg://
    # Example: postgresql+asyncpg://user:pass@host.render.com:5432/dbname
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/decoraai"

    # ── Auth ─────────────────────────────────────────────────────────────────
    jwt_secret: str = "dev-secret-change-in-production-at-least-32-chars"
    jwt_algorithm: str = "HS256"
    jwt_expire_days: int = 7

    # ── CORS ─────────────────────────────────────────────────────────────────
    cors_origins: list[str] = ["http://localhost:3000"]

    # ── Diffusion model (LoRA) ────────────────────────────────────────────────
    # Path to the base Stable Diffusion model (HuggingFace repo id OR local path)
    # e.g. "runwayml/stable-diffusion-v1-5"  or  "/models/sd-v1-5"
    sd_base_model: str = "runwayml/stable-diffusion-v1-5"

    # Path to your LoRA weights directory or .safetensors file
    # e.g. "/models/my-floorplan-lora"  or  "./assets/lora/floorplan.safetensors"
    lora_weights_path: str = "./assets/lora"

    # LoRA adapter name (used when loading from a directory with multiple adapters)
    lora_adapter_name: str = "floorplan_lora"

    # LoRA scale — how strongly the LoRA influences generation (0.0 – 1.0)
    lora_scale: float = 0.85

    # Image generation defaults
    image_width: int = 512
    image_height: int = 512
    image_steps: int = 30
    image_guidance_scale: float = 7.5

    # Device override: "auto" | "cuda" | "mps" | "cpu"
    device: Literal["auto", "cuda", "mps", "cpu"] = "auto"

    # Whether to load the model at startup (set False to skip in dev without GPU)
    model_enabled: bool = True

    # ── Chat ─────────────────────────────────────────────────────────────────
    # Plug your LLM details here (optional — backend has a placeholder by default)
    chat_enabled: bool = False  # flip to True once you wire up an LLM
    # openai_api_key: str = ""
    # openai_model: str = "gpt-4o"


@lru_cache
def get_settings() -> Settings:
    return Settings()
