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

    # ── PostgreSQL (auth / users) ─────────────────────────────────────────────
    # Render external URL — change scheme to postgresql+asyncpg://
    # Example: postgresql+asyncpg://user:pass@host.render.com:5432/dbname
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/decoraai"

    # ── MongoDB Atlas (messages / history) ───────────────────────────────────
    # Atlas connection string from: Cluster → Connect → Drivers
    # Example: mongodb+srv://user:pass@cluster0.xxxxx.mongodb.net/?retryWrites=true
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "DecoraAI"

    # ── Auth ─────────────────────────────────────────────────────────────────
    jwt_secret: str = "dev-secret-change-in-production-at-least-32-chars"
    jwt_algorithm: str = "HS256"
    jwt_expire_days: int = 7

    # ── CORS ─────────────────────────────────────────────────────────────────
    cors_origins: list[str] = ["http://localhost:3000"]

    # ── Diffusion model (LoRA) ────────────────────────────────────────────────
    sd_base_model: str = "runwayml/stable-diffusion-v1-5"
    lora_weights_path: str = "./assets/lora"
    lora_adapter_name: str = "floorplan_lora"
    lora_scale: float = 0.85
    image_width: int = 512
    image_height: int = 512
    image_steps: int = 30
    image_guidance_scale: float = 7.5
    device: Literal["auto", "cuda", "mps", "cpu"] = "auto"
    model_enabled: bool = False

    # ── Chat ─────────────────────────────────────────────────────────────────
    chat_enabled: bool = False
    # openai_api_key: str = ""
    # openai_model: str = "gpt-4o"
    # anthropic_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
