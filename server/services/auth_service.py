"""
services/auth_service.py
------------------------
Auth business logic backed by PostgreSQL via async SQLAlchemy.

Public interface (unchanged from the in-memory version):
  register_user(req, db)  → TokenResponse
  login_user(req, db)     → TokenResponse
  get_user_by_id(id, db)  → UserResponse | None

The routers pass in an AsyncSession from Depends(get_db); nothing
else in the codebase needs to know about the DB.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password, verify_password, create_access_token, new_id
from db import UserRow, find_user_by_email, find_user_by_id
from models.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse


# ── Exceptions ────────────────────────────────────────────────────────────────

class AuthError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


# ── Public API ────────────────────────────────────────────────────────────────

async def register_user(req: RegisterRequest, db: AsyncSession) -> TokenResponse:
    email = req.email.strip().lower()

    existing = await find_user_by_email(email, db)
    if existing:
        raise AuthError("Email already registered", status_code=409)

    row = UserRow(
        id=new_id(),
        name=req.name.strip(),
        email=email,
        password_hash=hash_password(req.password),
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)

    return _build_token_response(row)


async def login_user(req: LoginRequest, db: AsyncSession) -> TokenResponse:
    email = req.email.strip().lower()
    row = await find_user_by_email(email, db)

    if not row or not verify_password(req.password, row.password_hash):
        raise AuthError("Invalid email or password", status_code=401)

    return _build_token_response(row)


async def get_user_by_id(user_id: str, db: AsyncSession) -> UserResponse | None:
    row = await find_user_by_id(user_id, db)
    if row is None:
        return None
    return UserResponse(id=row.id, name=row.name, email=row.email)


# ── Internal helpers ──────────────────────────────────────────────────────────

def _build_token_response(row: UserRow) -> TokenResponse:
    user = UserResponse(id=row.id, name=row.name, email=row.email)
    token = create_access_token({"sub": row.id, "email": row.email, "name": row.name})
    return TokenResponse(access_token=token, user=user)
