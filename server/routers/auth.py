"""
routers/auth.py
---------------
POST /api/auth/register  →  { access_token, token_type, user }
POST /api/auth/login     →  { access_token, token_type, user }
GET  /api/auth/me        →  { id, name, email }
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from db import get_db
from models.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from services.auth_service import AuthError, get_user_by_id, login_user, register_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
)
async def register(
        body: RegisterRequest,
        db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    try:
        return await register_user(body, db)
    except AuthError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate and receive a JWT",
)
async def login(
        body: LoginRequest,
        db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    try:
        return await login_user(body, db)
    except AuthError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Return the currently authenticated user",
)
async def me(
        current_user: dict = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
) -> UserResponse:
    user = await get_user_by_id(current_user["sub"], db)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
