"""
db.py
-----
Database engine, session factory, ORM models, and schema initialisation.

Everything database-related lives here so auth_service.py stays focused
on business logic. Other services can import `AsyncSession` and `get_db`
when they need DB access.
"""

from __future__ import annotations

from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.config import get_settings

settings = get_settings()

# ── Engine & session factory ──────────────────────────────────────────────────

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,  # logs SQL when DEBUG=true
    pool_pre_ping=True,  # reconnect after idle/dropped connections
    pool_size=5,
    max_overflow=10,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# ── Base ──────────────────────────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


# ── ORM models ────────────────────────────────────────────────────────────────

class UserRow(Base):
    """Persisted user account."""
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)


# ── Schema initialisation ─────────────────────────────────────────────────────

async def init_db() -> None:
    """
    Create all tables if they don't already exist.
    Safe to call on every startup — uses CREATE TABLE IF NOT EXISTS semantics.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ── Session dependency ────────────────────────────────────────────────────────

async def get_db() -> AsyncSession:  # type: ignore[return]
    """
    FastAPI dependency that yields an async DB session per request.

    Usage in a router:
        from db import get_db
        from sqlalchemy.ext.asyncio import AsyncSession

        @router.get("/example")
        async def example(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session


# ── Helper queries (shared across services) ───────────────────────────────────

async def find_user_by_email(email: str, db: AsyncSession) -> UserRow | None:
    result = await db.execute(select(UserRow).where(UserRow.email == email))
    return result.scalar_one_or_none()


async def find_user_by_id(user_id: str, db: AsyncSession) -> UserRow | None:
    result = await db.execute(select(UserRow).where(UserRow.id == user_id))
    return result.scalar_one_or_none()
