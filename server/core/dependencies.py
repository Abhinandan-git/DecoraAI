"""
core/dependencies.py
--------------------
Reusable FastAPI dependency functions.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.security import decode_access_token

bearer = HTTPBearer(auto_error=False)


def get_current_user(
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> dict:
    """
    Validates the Bearer JWT from the Authorization header.
    Returns the decoded payload dict.

    Usage:
        @router.get("/protected")
        def protected(user: dict = Depends(get_current_user)):
            ...
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


def get_optional_user(
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> dict | None:
    """Like get_current_user but returns None instead of raising for public endpoints."""
    if credentials is None:
        return None
    return decode_access_token(credentials.credentials)
