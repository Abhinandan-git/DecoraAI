"""
core/security.py
----------------
Password hashing and JWT creation / verification.
Uses HMAC-SHA256 for passwords (dev-grade in-memory store)
and python-jose for JWTs.
"""

import hashlib
import hmac
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

from core.config import get_settings

settings = get_settings()


# ── Password ──────────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    """HMAC-SHA256 password hash — sufficient for the in-memory dev store."""
    return hmac.new(
        settings.jwt_secret.encode(),
        password.encode(),
        hashlib.sha256,
    ).hexdigest()


def verify_password(plain: str, hashed: str) -> bool:
    return hmac.compare_digest(hash_password(plain), hashed)


# ── JWT ───────────────────────────────────────────────────────────────────────

def create_access_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.jwt_expire_days)
    payload["exp"] = expire
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except JWTError:
        return None


# ── ID factory ────────────────────────────────────────────────────────────────

def new_id() -> str:
    return str(uuid.uuid4())
