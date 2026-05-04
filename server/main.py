"""
main.py
-------
Application factory for the DecoraAI FastAPI backend.

Run in development:
    uvicorn main:app --reload --port 8000

Run in production:
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1

Note: use --workers 1 when the diffusion pipeline is enabled.
Multiple workers each load their own pipeline, multiplying VRAM usage.
Use a process manager (e.g. gunicorn + uvicorn worker) if you need
concurrency and have the VRAM to spare.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from db import init_db
from routers import auth, catalogue, chat, image
from services.image_service import load_pipeline, unload_pipeline

settings = get_settings()


# ── Lifespan (startup / shutdown) ─────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()  # create tables if they don't exist
    load_pipeline()  # load diffusion model (no-op if MODEL_ENABLED=false)
    yield
    # Shutdown
    unload_pipeline()


# ── App factory ───────────────────────────────────────────────────────────────

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Backend API for the DecoraAI floor plan editor.\n\n"
            "- **Auth** — JWT-based email/password authentication\n"
            "- **Catalogue** — SVG floor plan element library\n"
            "- **Image** — LoRA-augmented Stable Diffusion generation\n"
            "- **Chat** — Pluggable LLM assistant\n"
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # ── CORS ─────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Routers ───────────────────────────────────────────────────────────────
    app.include_router(auth.router)
    app.include_router(catalogue.router)
    app.include_router(image.router)
    app.include_router(chat.router)

    # ── Health check ─────────────────────────────────────────────────────────
    @app.get("/health", tags=["meta"], summary="Server health check")
    def health():
        return {
            "status": "ok",
            "version": settings.app_version,
            "model_enabled": settings.model_enabled,
            "chat_enabled": settings.chat_enabled,
        }

    return app


app = create_app()
